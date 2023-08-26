import "../../components/{{ entity_lower}}/form"
import "../../partials/Sidebar"
import "../../services/api"
import "react"
import "react-router-dom"
import Form
import React
import Sidebar
import {get{{ entity }}}
import {useParams}

function {{ entity }}Edit() {
    const { id } = useParams();

    {% for field in schema_fields_capitalize %}const [{{ field }}, set{{ field }}] = React.useState("")
    {% endfor %}

    React.useEffect(()=> {
        get{{ entity }}(id).then((data)=> {
            {% for field in schema_fields_capitalize %}set{{ field }}(data.{{ field }})
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