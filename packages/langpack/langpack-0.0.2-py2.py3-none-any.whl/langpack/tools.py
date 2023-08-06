import pkgutil
import importlib
import inspect
import json
import sys

import os
import time
import pickle
import json
import inspect
import shutil
import imp
import pkgutil
import importlib
import inspect
import argparse

from langpack.utils import format, build_lib, find_obj_dynamic, launch_api

agent_dir = "agent"
chain_dir = "chain"
embedding_dir = "embedding"
request_wrapper_dir = "request_wrapper"
vectorstore_dir = "vectorstore"
static_dir = "static"
tool_dir = "tool"
memory_dir = "memory"
utility_dir = "utility"

list_api_keys = {
    "serpapi_api_key": os.environ["SERPAPI_API_KEY"],
    "openai_api_key": os.environ["OPENAI_API_KEY"],
}


def delete_and_create(dir_path):
    if os.path.exists(dir_path):
        # If it does, delete it and recreate it
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)
    else:
        # If it doesn't, create it
        os.makedirs(dir_path)


def print_success(app_path):
    print(
        """
                  .--.           .---.        .-.
       .---|--|   .-.     | L |  .---. |~|    .--.
    .--|===|  |---|_|--.__| A |--|:::| |~|-==-|==|---.
    |%%|   |  |===| |~~|%%| M |--|   |_|~|    |  |___|-.
    |  |   |  |===| |==|  | B |  |:::|=| |    |  |---|=|
    |  |   |  |   |_|__|  | D |__|   | | |    |  |___| |
    |~~|===|--|===|~|~~|%%| A |--|:::|=|~|----|==|---|=|
    ^--^---'--^---^-^--^--^---'--^---^-^-^-==-^--^---^-"""
    )
    print(f"You app has been saved to {app_path}")
    print("--------------------------------------")
    print(f"You can run the following command to test it: ")
    print(
        f"cd {app_path} && python -c 'from langpack.tester import test_package; test_package()' && cd - >/dev/null"
    )
    print("--------------------------------------")
    print(f"Deploy the API: ")
    print(f"deploy {app_path}")


def replace_word_in_file(file_path, old_word, new_word):
    with open(file_path, "r") as file:
        file_text = file.read()

    # Replace the old word with the new word in the file text
    new_file_text = file_text.replace(old_word, new_word)

    with open(file_path, "w") as file:
        file.write(new_file_text)


def list_classes(module_name):
    try:
        module = importlib.import_module(module_name)
        classes = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                classes.append(obj)

        for loader, name, is_pkg in pkgutil.walk_packages(module.__path__):
            full_name = module_name + "." + name
            if is_pkg:
                classes += list_classes(full_name)
            else:
                try:
                    sub_module = importlib.import_module(full_name)
                    for name, obj in inspect.getmembers(sub_module, inspect.isclass):
                        if obj.__module__ == full_name:
                            classes.append(obj)
                except:
                    print(f"module {full_name} can not be loaded.")
    except:
        print(f"module {module_name} can not be loaded.")
    return classes


def list_classes_from_file(module_name):
    module = importlib.import_module(module_name)
    filename = inspect.getfile(module)
    classes = [
        obj
        for name, obj in inspect.getmembers(module, inspect.isclass)
        if inspect.getfile(obj) == filename
    ]
    return classes


def list_functions_from_file(module_name):
    # Load the module
    spec = importlib.util.spec_from_file_location("module.name", module_name + ".py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get all the functions defined in the module
    functions = inspect.getmembers(module, inspect.isfunction)

    # Filter out imported modules and the main function
    functions = [
        function[0]
        for function in functions
        if function[0] not in ("main", "__builtins__")
        and function[1].__module__ == module.__name__
    ]

    return functions


def is_list_of_strings(obj):
    if not isinstance(obj, list):
        return False
    return all(isinstance(item, str) for item in obj)


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


def pack_function(obj, dict_class):
    if not obj.__module__:
        obj.__module__ = os.environ["SOURCE_NAME"]
    obj_dict = {
        "type": "function",
        "deps": {},
        "kwargs": {"path": obj.__module__ + "." + obj.__name__},
    }

    return obj_dict


def pack_method(obj, dict_class):
    obj_dict = {
        "type": "method",
        "deps": {"__self__": _serialize(obj.__self__, dict_class)},
        "kwargs": {"__func__.__name__": obj.__func__.__name__},
    }
    return obj_dict


def pack_general(obj, dict_class):
    if hasattr(obj, "__dict__"):
        return _serialize(obj, dict_class)
    else:
        return None


def unpack_embedding(dict, upacked_dict, dict_class):
    module_name = ".".join(dict["type"].split(".")[:-1])
    class_name = dict["type"].split(".")[-1]
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    # delete redundant key
    if "model" in upacked_dict:
        if "document_model_name" in upacked_dict:
            del upacked_dict["document_model_name"]
        if "query_model_name" in upacked_dict:
            del upacked_dict["query_model_name"]

    argspec = inspect.getfullargspec(class_obj.__init__).args[1:]
    if argspec:
        upacked_dict = {k: v for k, v in upacked_dict.items() if k in argspec}

    obj = class_obj(**upacked_dict)
    return obj


def unpack_vectorstore(dict, upacked_dict, dict_class):
    module_name = ".".join(dict["type"].split(".")[:-1])
    class_name = dict["type"].split(".")[-1]
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    # Load from persistent storage
    if "retriever" in str(class_obj).lower():
        argspec = inspect.getfullargspec(class_obj.__init__).args[1:]
        if argspec:
            upacked_dict = {k: v for k, v in upacked_dict.items() if k in argspec}
        obj = class_obj(**upacked_dict)
    else:
        if "chroma" in str(class_obj).lower():
            obj = class_obj(
                persist_directory=upacked_dict["_persist_directory"],
                embedding_function=upacked_dict["_embedding_function"]
                if "_embedding_function" in upacked_dict
                else None,
            )
        elif "faiss" in str(class_obj).lower():
            obj = class_obj.load_local(
                folder_path=os.environ["VECTORSTORE_DIR"],
                embeddings=upacked_dict["embedding_function"].__self__,
            )
    return obj


def unpack_function(dict, upacked_dict, dict_class):
    function_path = dict["kwargs"]["path"]
    module_path = ".".join(function_path.split(".")[:-1])
    func_name = function_path.split(".")[-1]
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def unpack_method(dict, upacked_dict, dict_class):
    self_obj = _deserialize(dict["deps"]["__self__"], dict_class)
    return getattr(self_obj, dict["kwargs"]["__func__.__name__"])


def unpack_general(dict, upacked_dict, dict_class):
    module_name = ".".join(dict["type"].split(".")[:-1])
    class_name = dict["type"].split(".")[-1]
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    argspec = inspect.getfullargspec(class_obj.__init__).args[1:]
    if argspec:
        upacked_dict = {k: v for k, v in upacked_dict.items() if k in argspec}

    obj = class_obj(**upacked_dict)
    return obj


map_type_to_pack = {
    "chain": pack_general,
    "agent": pack_general,
    "embedding": pack_general,
    "memory": pack_general,
    "request_wrapper": pack_general,
    "tool": pack_general,
    "vectorstore": pack_general,
    "prompt": pack_general,
    "llm": pack_general,
    "custom": pack_general,
    "chatmodel": pack_general,
    "index": pack_general,
    "docstore": pack_general,
    "function": pack_function,
    "method": pack_method,
    "utility": pack_general,
}


map_type_to_unpack = {
    "chain": unpack_general,
    "agent": unpack_general,
    "embedding": unpack_embedding,
    "memory": unpack_general,
    "request_wrapper": unpack_general,
    "tool": unpack_general,
    "vectorstore": unpack_vectorstore,
    "prompt": unpack_general,
    "llm": unpack_general,
    "custom": unpack_general,
    "chatmodel": unpack_general,
    "memory": unpack_general,
    "index": unpack_general,
    "docstore": unpack_general,
    "function": unpack_function,
    "method": unpack_method,
    "utility": unpack_general,
}


def get_type(type_name, dict_class):
    type_name = type_name.split(".")[-1]
    if type_name in dict_class["list_class_chain"]:
        return "chain"
    elif type_name in dict_class["list_class_agent"]:
        return "agent"
    elif type_name in dict_class["list_class_vectorstore"]:
        return "vectorstore"
    elif type_name in dict_class["list_class_embedding"]:
        return "embedding"
    elif type_name in dict_class["list_class_requestwrapper"]:
        return "request_wrapper"
    elif type_name in dict_class["list_class_tool"]:
        return "tool"
    elif type_name in dict_class["list_class_memory"]:
        return "memory"
    elif type_name in dict_class["list_class_prompt"]:
        return "prompt"
    elif type_name in dict_class["list_class_llm"]:
        return "llm"
    elif type_name in dict_class["list_class_custom"]:
        return "custom"
    elif type_name in dict_class["list_class_chatmodel"]:
        return "chatmodel"
    elif type_name in dict_class["list_class_index"]:
        return "index"
    elif type_name in dict_class["list_class_docstore"]:
        return "docstore"
    elif type_name in dict_class["list_class_function"]:
        return "function"
    elif type_name in dict_class["list_class_method"]:
        return "method"
    elif type_name in dict_class["list_class_utility"]:
        return "utility"
    elif type_name == "list":
        return "list"
    else:
        raise Exception(f"langpack doesn't support type {type_name}")


def _serialize(obj, dict_class):
    if isinstance(obj, list):
        if is_list_of_strings(obj):
            return obj
        else:
            return [_serialize(item, dict_class) for item in obj]

    obj_type = str(type(obj))[8:-2]

    # patch name of the source script to the object type, otherwise can't be imported during unpack
    if obj_type in dict_class["list_class_custom"]:
        obj_type = os.environ["SOURCE_NAME"] + "." + obj_type

    # deps: attributes that are in the list_class that need special instantiation
    # kwargs: json serializable attributes that are not in the list_class
    obj_dict = {"type": obj_type, "deps": {}, "kwargs": {}}
    for key, value in vars(obj).items():
        type_name = str(type(getattr(obj, key)))[8:-2]

        if not type_name == "NoneType":
            type_name = type_name.split(".")[-1]

        if not type_name in dict_class["list_class"]:
            if is_json_serializable(value) and not key in list_api_keys:
                obj_dict["kwargs"][key] = value
            else:
                print(
                    f"WARNING: {obj_type} . {type_name} not in list_class and not JSON serializable"
                )
            continue

        if isinstance(value, (list, tuple)):
            if is_json_serializable(value):
                obj_dict["kwargs"][key] = value
            else:
                obj_dict["deps"][key] = _serialize(value, dict_class)
        else:
            pack_func = map_type_to_pack[get_type(type_name, dict_class)]
            obj_packed = pack_func(value, dict_class)
            if obj_packed:
                obj_dict["deps"][key] = obj_packed

    return obj_dict


def _deserialize(dependency_dict, dict_class):
    if not dependency_dict:
        return None

    if isinstance(dependency_dict, (list, tuple)):
        objs = []
        for item in dependency_dict:
            objs.append(_deserialize(item, dict_class))
        return objs

    deps = {}
    for key, value in dependency_dict["deps"].items():
        deps[key] = _deserialize(value, dict_class)

    obj_type = dependency_dict["type"]
    unpack_func = map_type_to_unpack[get_type(obj_type, dict_class)]
    obj = unpack_func(
        dependency_dict, {**deps, **dependency_dict["kwargs"]}, dict_class
    )

    return obj


def create_dict_deps(filename):
    dict_class = {
        "list_class_llm": [c.__name__ for c in list_classes("langchain.llms")],
        "list_class_prompt": [c.__name__ for c in list_classes("langchain.prompts")],
        "list_class_utility": [c.__name__ for c in list_classes("langchain.utilities")],
        "list_class_chain": [c.__name__ for c in list_classes("langchain.chains")],
        "list_class_agent": [c.__name__ for c in list_classes("langchain.agents")],
        "list_class_vectorstore": [
            c.__name__ for c in list_classes("langchain.vectorstores")
        ],
        "list_class_embedding": [
            c.__name__ for c in list_classes("langchain.embeddings")
        ],
        "list_class_requestwrapper": [
            c.__name__ for c in list_classes_from_file("langchain.requests")
        ],
        "list_class_tool": [c.__name__ for c in list_classes("langchain.tools")],
        "list_class_memory": [c.__name__ for c in list_classes("langchain.memory")],
        "list_class_custom": [c.__name__ for c in list_classes_from_file(filename)],
        "list_class_chatmodel": [
            c.__name__ for c in list_classes("langchain.chat_models")
        ],
        "list_class_memory": [c.__name__ for c in list_classes("langchain.memory")],
        "list_class_index": [c.__name__ for c in list_classes("langchain.indexes")],
        "list_class_docstore": [c.__name__ for c in list_classes("langchain.docstore")],
        "list_class_function": ["function"],
        "list_class_method": ["method"],
    }

    dict_class["list_class_agent"].remove("Tool")
    dict_class["list_class_tool"].append("Tool")

    dict_class["list_class"] = (
        ["list"]
        + dict_class["list_class_llm"]
        + dict_class["list_class_prompt"]
        + dict_class["list_class_utility"]
        + dict_class["list_class_chain"]
        + dict_class["list_class_agent"]
        + dict_class["list_class_vectorstore"]
        + dict_class["list_class_embedding"]
        + dict_class["list_class_requestwrapper"]
        + dict_class["list_class_tool"]
        + dict_class["list_class_memory"]
        + dict_class["list_class_chatmodel"]
        + dict_class["list_class_memory"]
        + dict_class["list_class_index"]
        + dict_class["list_class_docstore"]
        + dict_class["list_class_function"]
        + dict_class["list_class_method"]
        + dict_class["list_class_custom"]
    )

    return dict_class


def pack():
    """
    Takes a Python langchain script file path as the input and pack the app.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path", help="Python script file path")
    args = parser.parse_args()

    # Setup the path
    script_path = args.script_path
    module_path, ext = os.path.splitext(script_path)

    # use script_path as the working directory
    os.chdir(os.path.join(os.getcwd(), "/".join(module_path.split("/")[:-1])))
    current_directory = os.getcwd()

    # update sys.path so the script can be imported (needed for gethering custom classes implemented in that file)
    sys.path.insert(0, current_directory)

    script_path = os.path.basename(script_path)
    module_path, ext = os.path.splitext(script_path)

    app_name = module_path.split(".")[-1]
    os.environ["SOURCE_NAME"] = app_name
    print(f"script_path: {script_path}")
    print(f"app_name: {app_name}")
    print(f"current_directory: {current_directory}")
    print("Import search paths: ------------------")
    for path in sys.path:
        print(path)

    # Build lib_script.py
    lib_script_path = build_lib(script_path)
    lib_module_path, ext = os.path.splitext(lib_script_path)
    print(f"lib_module_path: {lib_module_path}")
    print("---------------------------------------")

    # build a dict_class
    dict_class = create_dict_deps(lib_module_path)
    print("list_class: ")
    print(dict_class["list_class"])
    print("list_class_custom: ")
    print(dict_class["list_class_custom"])
    print("---------------------------------------")

    # Run the script and get the obj of interests
    obj_name, obj_type, obj = find_obj_dynamic(script_path, dict_class["list_class"])

    print("Object of interest: ")
    print(f"obj_name: {obj_name}")
    print(f"obj_type: {obj_type}")
    print(obj)
    print("---------------------------------------")

    if not obj_name:
        raise ValueError("No object of interests can be found.")

    # pack
    os.environ["APP_DIR"] = "apps/{}_{}".format(
        app_name, time.strftime("%Y%m%d-%H%M%S")
    )

    delete_and_create(os.environ["APP_DIR"])
    delete_and_create(static_dir)
    delete_and_create(memory_dir)

    # pack: serialize
    dependency_dict = _serialize(obj, dict_class)

    print("---------------------------------------")
    print("dependency_dict: ")
    print(json.dumps(dependency_dict, indent=4))
    print("---------------------------------------")

    app = {}
    app["source_name"] = app_name
    app["dependency_dict"] = dependency_dict

    with open("app.json", "w") as json_file:
        json.dump(app, json_file, indent=4)

    replace_word_in_file("app.json", "__main__", lib_module_path)

    # pack: create by-products
    _, langpack_path, _ = imp.find_module("langpack")

    app_template_path = os.path.abspath(langpack_path) + "/app_template.py"
    app_py_path = os.path.join(os.environ["APP_DIR"], "app.py")
    shutil.copy2(app_template_path, app_py_path)

    client_template_path = os.path.abspath(langpack_path) + "/client_template.py"
    client_py_path = os.path.join(os.environ["APP_DIR"], "client.py")
    shutil.copy2(client_template_path, client_py_path)

    index_template_path = os.path.abspath(langpack_path) + "/index.html"
    index_path = os.path.join(static_dir, "index.html")
    shutil.copy2(index_template_path, index_path)

    # pack: filling input and output to templates
    input_key = None
    output_key = None

    if app["dependency_dict"]["type"].split(".")[-1] == "AgentExecutor":
        input_key = '"input"'
        output_key = '"output"'
    elif app["dependency_dict"]["type"].split(".")[-1] == "BabyAGI":
        input_key = '"objective"'
        output_key = '"output"'
    else:
        if "input_key" in app["dependency_dict"]["kwargs"]:
            input_key = '"' + app["dependency_dict"]["kwargs"]["input_key"] + '"'
        elif "question_key" in app["dependency_dict"]["kwargs"]:
            input_key = '"' + app["dependency_dict"]["kwargs"]["question_key"] + '"'
        else:
            raise Exception(f"can't find input_key for app")

        if "output_key" in app["dependency_dict"]["kwargs"]:
            output_key = '"' + app["dependency_dict"]["kwargs"]["output_key"] + '"'
        else:
            raise Exception(f"can't find output_key for app")

    if input_key:
        replace_word_in_file(app_py_path, "{input_key}", input_key)
        replace_word_in_file(client_py_path, "{input_key}", input_key)
        replace_word_in_file(index_path, "$input_key$", input_key)
    if output_key:
        replace_word_in_file(app_py_path, "{output_key}", output_key)
        replace_word_in_file(client_py_path, "{output_key}", output_key)
        replace_word_in_file(index_path, "$output_key$", output_key)

    app_script_path = os.path.join(os.environ["APP_DIR"], script_path)
    shutil.copy2(script_path, app_script_path)

    shutil.move(lib_module_path + ".py", os.environ["APP_DIR"])

    init_path = os.path.join(os.environ["APP_DIR"], "__init__.py")
    with open(init_path, "w") as f:
        pass

    if os.path.exists(vectorstore_dir):
        shutil.move(vectorstore_dir, os.environ["APP_DIR"])
    shutil.move(static_dir, os.environ["APP_DIR"])
    shutil.move(memory_dir, os.environ["APP_DIR"])

    shutil.move("app.json", os.environ["APP_DIR"])

    # print success msg and test command
    print_success(os.path.join(os.getcwd(), os.environ["APP_DIR"]))


def unpack(app_config_path):
    current_directory = os.getcwd()
    # update sys.path so the script can be imported
    # (needed for gethering custom classes implemented in that file)
    sys.path.insert(0, current_directory)

    print(f"current_directory: {current_directory}")
    print("Import search paths: ------------------")
    for path in sys.path:
        print(path)
    print("---------------------------------------")

    with open(app_config_path, "r") as f:
        # Load the JSON data into a Python dictionary
        app_config = json.load(f)
        print(app_config)

    dict_class = create_dict_deps("lib_" + app_config["source_name"])

    return _deserialize(app_config["dependency_dict"], dict_class)


def deploy():
    """
    Takes a package path and launch a flask backend service and a client to post request
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("app_path", help="Python script file path")
    args = parser.parse_args()

    commands = [
        f"cd {args.app_path} && source $VIRTUAL_ENV/bin/activate && python app.py",
        f"cd {args.app_path} && source $VIRTUAL_ENV/bin/activate && python client.py",
    ]

    launch_api(commands)
