import ast
from astunparse import Unparser as OriginalUnparser
import io
import astpretty
import astor
import os
import sys
from types import FunctionType
import subprocess


class Unparser(OriginalUnparser):
    def _Constant(self, t):
        if isinstance(t.value, str):
            self.write(repr(t.value))
        else:
            self.write(repr(t.value))


def unparse_ast(tree):
    v = io.StringIO()
    Unparser(tree, file=v)
    return v.getvalue()


def format(input_file: str, output_file: str = None):
    if output_file is None:
        output_file = input_file.replace(".py", "_formatted.py")

    with open(input_file, "r") as file:
        code = file.read()

    tree = ast.parse(code)

    imports = []
    functions = []
    classes = []
    main_code = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node)
        elif isinstance(node, ast.ClassDef):
            classes.append(node)
        else:
            main_code.append(node)

    update_globals = ast.Expr(
        ast.Call(
            func=ast.Attribute(
                value=ast.Call(
                    func=ast.Name(id="globals", ctx=ast.Load()), args=[], keywords=[]
                ),
                attr="update",
                ctx=ast.Load(),
            ),
            args=[],
            keywords=[
                ast.keyword(
                    arg=None,
                    value=ast.Dict(
                        keys=[ast.Constant(value="app")],
                        values=[ast.Name(id="app", ctx=ast.Load())],
                    ),
                )
            ],
        )
    )

    return_app = ast.Return(value=ast.Name(id="app", ctx=ast.Load()))

    main_function = ast.FunctionDef(
        name="main",
        args=ast.arguments(
            args=[],
            posonlyargs=[],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=main_code + [update_globals, return_app],
        decorator_list=[],
        returns=None,
    )

    main_condition = ast.If(
        test=ast.Compare(
            left=ast.Name(id="__name__", ctx=ast.Load()),
            ops=[ast.Eq()],
            comparators=[ast.Constant(value="__main__")],
        ),
        body=[
            ast.Expr(
                ast.Call(func=ast.Name(id="main", ctx=ast.Load()), args=[], keywords=[])
            )
        ],
        orelse=[],
    )

    tree.body = imports + functions + classes + [main_function, main_condition]

    formatted_code = unparse_ast(tree)

    with open(output_file, "w") as file:
        file.write(formatted_code)


def find_obj(script_path, class_list):
    with open(script_path, "r") as f:
        script = f.read()

    tree = ast.parse(script)

    astpretty.pprint(tree, indent=4, show_offsets=False)

    class_assignments = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if (
                isinstance(node.value.func, ast.Name)
                and node.value.func.id in class_list
            ):
                target = node.targets[0]
                if isinstance(target, ast.Name):
                    class_assignments.append((target.id, node.value.func.id))
            if (
                isinstance(node.value.func, ast.Attribute)
                and not isinstance(node.value.func.value, ast.Constant)
                and not isinstance(node.value.func.value, ast.Call)
                and not isinstance(node.value.func.value, ast.Subscript)
                and not isinstance(node.value.func.value, ast.Attribute)
                and node.value.func.value.id in class_list
            ):
                target = node.targets[0]
                if isinstance(target, ast.Name):
                    class_assignments.append((target.id, node.value.func.value.id))

    return class_assignments[-1] if class_assignments else None


def find_obj_dynamic(script_path, class_list):
    # Add the script's directory to the system path
    script_dir = os.path.dirname(script_path)
    sys.path.append(script_dir)

    # Read the script file
    with open(script_path, "r") as f:
        script = f.read()

    # change working dir to the script's directory in cas there are reference path for other code/data
    os.chdir(os.path.join(os.getcwd(), "/".join(script_path.split("/")[:-1])))
    current_directory = os.getcwd()
    print(current_directory)

    # Create a custom namespace for executing the script
    namespace = {}

    # Execute the script in the custom namespace
    # XXX: THIS IS DANGEROUS
    exec(script, namespace)

    # Remove the script's directory from the system path
    sys.path.remove(script_dir)

    # Iterate over the namespace items and filter objects based on class names
    matching_objects = [
        (name, obj.__class__.__name__, obj)
        for name, obj in namespace.items()
        if obj.__class__.__name__ in class_list and not isinstance(obj, FunctionType)
    ]

    # Return the last matching object or None if no matches are found
    return matching_objects[-1] if matching_objects else (None, None, None)


def build_lib(path):
    print("-----------------------------------------")
    print(path)
    print("-----------------------------------------")
    # Parse the source code of the script
    with open(path, "r") as f:
        tree = ast.parse(f.read())

    # Extract the necessary imports, function and class definitions
    imports = []
    defs = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(node)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node)
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            defs.append(node)

    # Generate the code for the library file
    code = ast.Module(body=imports + defs)
    lib_path = "lib_" + os.path.basename(path)
    with open(lib_path, "w") as f:
        f.write(astor.to_source(code))
    return lib_path


def launch_api(shell_commands):
    if not shell_commands:
        print("No shell commands provided")
        return

    # Start a new terminal and create a new tmux session
    terminal = subprocess.Popen(
        [
            "gnome-terminal",
            "--",
            "tmux",
            "new-session",
            "-s",
            "api_session",
            "-n",
            "window0",
            "-d",
        ]
    )
    terminal.wait()

    # Run the first command in the first window
    subprocess.run(
        [
            "tmux",
            "send-keys",
            "-t",
            "api_session:window0",
            f"{shell_commands[0]}",
            "Enter",
        ]
    )

    # Create a new horizontal pane and run a command in it for the rest of the commands
    for command in shell_commands[1:]:
        subprocess.run(["tmux", "split-window", "-t", "api_session", "-h"])
        subprocess.run(
            ["tmux", "send-keys", "-t", "api_session", f"{command}", "Enter"]
        )

    # Adjust the layout of the panes to 'even-horizontal'
    subprocess.run(["tmux", "select-layout", "-t", "api_session", "even-horizontal"])

    # Attach to the tmux session
    subprocess.run(
        ["gnome-terminal", "--", "tmux", "attach-session", "-t", "api_session"]
    )
