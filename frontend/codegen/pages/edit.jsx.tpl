import Form from "../../components/{{ entity_lower}}/form"
import Sidebar from "../../partials/Sidebar";
import {useParams} from "react-router-dom";
import {get{{ entity }}} from "../../services/api";
import React from "react";
function {{ entity }}Edit() {
    const { id } = useParams();

    {% for field in schema_fields %}const [{{ field }}, set{{ schema_fields[field] }}] = React.useState("")
    {% endfor %}

    React.useEffect(()=> {
        get{{ entity }}(id).then((data)=> {
            {% for field in schema_fields %}set{{ schema_fields[field] }}(data.{{ field }})
            {% endfor %}
        })
    })
    return (<div className="flex h-[100dvh] overflow-hidden">
        <Sidebar/>
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <main className="grow">
                <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
                    <Form

                          {% for field in schema_fields %}{{ field }}={{ '{' }}{{ field }}{{ '}' }}
                          {% endfor %}

                          id={id}
                    />
                </div>
            </main>
        </div>
    </div>)
}

export default {{ entity }}Edit