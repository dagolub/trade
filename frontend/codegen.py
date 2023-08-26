import os
import re

import typer
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("frontend", package_path="codegen"),
    autoescape=select_autoescape(),
)


def snake_case_to_capitalize_every_letter(input_string):
    words = input_string.split("_")
    capitalized_words = [word.capitalize() for word in words]
    return "".join(capitalized_words)


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def pluralize(noun):
    if re.search("[sxz]$", noun):
        return re.sub("$", "es", noun)
    elif re.search("[^aeioudgkprt]h$", noun):
        return re.sub("$", "es", noun)
    elif re.search("[aeiouy]$", noun):
        return re.sub("y$", "ies", noun)
    else:
        return noun + "s"


def save_to_file(content, file_name):
    with open(file_name, "w") as f:
        f.write(content)


def get_file(file_name):
    if not os.path.isfile(file_name):
        print(f"File {file_name} does not exist!")
        exit(1)

    with open(file_name) as f:
        content = f.read()
    return content


def parse_model(model_name):
    model_file = get_file(f"../backend/app/app/models/{camel_to_snake(model_name)}.py")
    type_mapping = {
        "String": "str",
        "Integer": "int",
        "Date": "datetime.date",
        "Float": "float",
        "Boolean": "bool",
        "JSON": "list",
    }
    fields = re.findall("(\w+) = Column\((\w+)", model_file)  # noqa
    schema_fields = {}
    for field in fields:
        default = "None"
        set_default = False
        if 2 in field and field[2] == "default":
            default = field[3]
            set_default = True

        if 2 in field and 3 in field and field[2] == "nullable" and field[3] == "False":
            if set_default:
                new_field = f"{field[0]}: {type_mapping[field[1]]} = {default}"
            else:
                new_field = f"{field[0]}: {type_mapping[field[1]]}"
        else:
            new_field = f"{field[0]}: Optional[{type_mapping[field[1]]}] = {default}"

        if new_field[0:1] != "_" and "owner_id" not in new_field:
            schema_fields.setdefault(field[0], new_field)

    relations = re.findall(
        '(\w+) = relationship\("(\w+)", (back_populates|backref)="(\w+)"\)', model_file
    )  # noqa
    related_fields = {}
    for field in relations:
        related_fields.setdefault(
            field[0], {"related_model": field[1], "back_populates": field[2]}
        )
    return schema_fields, related_fields


def install_files(model_name, entity_lower, schema_fields):
    sidebar_file_path = "src/partials/Sidebar.jsx"
    sidebar_file = get_file(sidebar_file_path)
    fields_names = ", ".join([i for i in schema_fields if "_" not in i])
    if entity_lower not in sidebar_file:
        replace_to = (
            "<li className={li_class}>\n"
            '    <a href="/' + entity_lower + '/list" className={a_class}>\n'
            "        <span className={span_class}>\n"
            f"            {model_name}s\n"
            "        </span>\n"
            "    </a>\n"
            "</li>"
        )
        sidebar_file = re.sub(
            "Users</span></a></li>", f"\g<0>\n{replace_to}", sidebar_file
        )  # noqa
        save_to_file(sidebar_file.strip(), sidebar_file_path)
    else:
        print("No need update Sidebar.jsx")

    app_file_path = "src/App.jsx"
    app_file = get_file(app_file_path)
    if entity_lower not in app_file:
        replace_to = (
            f"import {model_name}s from './pages/{entity_lower}/list';\n"
            f"import {model_name}sNew from './pages/{entity_lower}/new';\n"
            f"import {model_name}sEdit from './pages/{entity_lower}/edit';\n"
        )
        app_file = re.sub("//INSERT_1", f"\n{replace_to}\n\g<0>", app_file)  # noqa
        save_to_file(app_file.strip(), app_file_path)

        replace_to = (
            f'        <Route path="/'
            + entity_lower
            + '/list" element={<'
            + model_name
            + "s />} />\n"
            f'        <Route path="/'
            + entity_lower
            + '/new" element={<'
            + model_name
            + "sNew />} />\n"
            f'        <Route path="/'
            + entity_lower
            + '/edit/:id" element={<'
            + model_name
            + "sEdit />} />"
        )
        app_file = re.sub("//INSERT_2", f"\n{replace_to}\n\g<0>", app_file)  # noqa
        save_to_file(app_file.strip(), app_file_path)

    else:
        print("No need update App.jsx")

    api_file_path = "src/services/api.js"
    api_file = get_file(api_file_path)
    if model_name not in api_file:
        replace_to = (
            f"const create{model_name} = ({fields_names})" + " => {\n"
            f"  return POST('/api/{entity_lower}/'," + " {\n"
        )
        for field in schema_fields:
            if "_" not in field:
                replace_to += f'        "{field}": {field},' + "\n"

        replace_to += (
            "})\n  }\n"
            f"const get{model_name}s" + ' = (q="", skip=0, limit=10) => {\n'
            f"  return GET('/api/{entity_lower}/?skip=' + skip + '&limit=' + limit + '&q=' + q)\n"
            "}\n"
            f"const get{model_name}" + " = (id) => {\n"
            f"   return GET('/api/{entity_lower}/' + id)\n"
            "}\n"
            f"const update{model_name} = (id, {fields_names})" + " => {\n"
            f"      return PUT('/api/{entity_lower}/'" + " + id, {\n"
        )
        for field in schema_fields:
            if "_" not in field:
                replace_to += f'        "{field}": {field},' + "\n"
        replace_to = (
            replace_to + "  })\n"
            "}\n"
            f"const delete{model_name}" + " = (id) => {\n"
            f"   return DELETE('/api/{entity_lower}/' + id)\n"
            "}"
        )
        api_file = re.sub("//INSERT1", f"\n{replace_to}\n\g<0>", api_file)  # noqa
        save_to_file(api_file.strip(), api_file_path)

        replace_to = f"create{model_name}, get{model_name}s, get{model_name}, update{model_name}, delete{model_name}"
        api_file = re.sub("//INSERT2", f"\n{replace_to}\n\g<0>", api_file)  # noqa
        save_to_file(api_file.strip(), api_file_path)
    else:
        print("No need update api.js")

    if not os.path.isdir(f"src/components/{entity_lower}/"):
        os.mkdir(f"src/components/{entity_lower}/")
    os.rename(
        f"codegen/generated/components_form_{entity_lower}.jsx",
        f"src/components/{entity_lower}/form.jsx",
    )
    os.rename(
        f"codegen/generated/components_table_{entity_lower}.jsx",
        f"src/components/{entity_lower}/{model_name}sTable.jsx",
    )
    os.rename(
        f"codegen/generated/components_table_item_{entity_lower}.jsx",
        f"src/components/{entity_lower}/{model_name}sTableItem.jsx",
    )

    if not os.path.isdir(f"src/pages/{entity_lower}/"):
        os.mkdir(f"src/pages/{entity_lower}/")
    os.rename(
        f"codegen/generated/pages_edit_{entity_lower}.jsx",
        f"src/pages/{entity_lower}/edit.jsx",
    )
    os.rename(
        f"codegen/generated/pages_list_{entity_lower}.jsx",
        f"src/pages/{entity_lower}/list.jsx",
    )
    os.rename(
        f"codegen/generated/pages_new_{entity_lower}.jsx",
        f"src/pages/{entity_lower}/new.jsx",
    )


def main(model_name: str):
    if model_name is None:
        model_name = typer.prompt("Please enter model name (Model)?")

    schema_fields, _ = parse_model(model_name)
    # schema_fields = [i for i in schema_fields if "_" not in i]
    schema_fields_capitalize = [i.capitalize() for i in schema_fields if "_" not in i]

    for field in schema_fields:
        schema_fields[field] = snake_case_to_capitalize_every_letter(field)
    # schema_fields = schema_fields_capitalize
    if not os.path.isdir("codegen/generated"):
        os.mkdir("codegen/generated")

    entity_lower = camel_to_snake(pluralize(model_name))

    components_form = env.get_template("components/form.jsx.tpl")
    save_to_file(
        components_form.render(
            entity=model_name,
            entity_lower=entity_lower,
            schema_fields=schema_fields,
            schema_fields_capitalize=schema_fields_capitalize,
        ),
        f"codegen/generated/components_form_{entity_lower}.jsx",
    )

    components_entity_table = env.get_template("components/EntityTable.jsx.tpl")
    save_to_file(
        components_entity_table.render(
            entity=model_name,
            entity_lower=entity_lower,
            schema_fields=schema_fields,
            schema_fields_capitalize=schema_fields_capitalize,
        ),
        f"codegen/generated/components_table_{entity_lower}.jsx",
    )

    components_entity_table_item = env.get_template(
        "components/EntityTableItem.jsx.tpl"
    )
    save_to_file(
        components_entity_table_item.render(
            entity=model_name,
            entity_lower=entity_lower,
            schema_fields=schema_fields,
            schema_fields_capitalize=schema_fields_capitalize,
        ),
        f"codegen/generated/components_table_item_{entity_lower}.jsx",
    )

    pages_edit = env.get_template("pages/edit.jsx.tpl")
    save_to_file(
        pages_edit.render(
            entity=model_name,
            entity_lower=entity_lower,
            schema_fields=schema_fields,
            schema_fields_capitalize=schema_fields_capitalize,
        ),
        f"codegen/generated/pages_edit_{entity_lower}.jsx",
    )

    pages_list = env.get_template("pages/list.jsx.tpl")
    save_to_file(
        pages_list.render(
            entity=model_name,
            entity_lower=entity_lower,
            schema_fields=schema_fields,
            schema_fields_capitalize=schema_fields_capitalize,
        ),
        f"codegen/generated/pages_list_{entity_lower}.jsx",
    )

    pages_new = env.get_template("pages/new.jsx.tpl")
    save_to_file(
        pages_new.render(
            entity=model_name,
            entity_lower=entity_lower,
            schema_fields=schema_fields,
            schema_fields_capitalize=schema_fields_capitalize,
        ),
        f"codegen/generated/pages_new_{entity_lower}.jsx",
    )

    is_install = typer.confirm("Install new files?")
    if is_install:
        install_files(model_name, entity_lower, schema_fields)


if __name__ == "__main__":
    typer.run(main)
