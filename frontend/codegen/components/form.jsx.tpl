import React from 'react';
import {create{{ entity }}, update{{ entity }}} from "../../services/api";

function Form({{ '{' }}{% for field in schema_fields %}{{field}} = "",{% endfor %}id=""{{'}'}}) {
    {% for field in schema_fields_capitalize %}const ref{{ field }} = React.useRef("")
    {% endfor %}
    const setResp = (resp) => {
        if( resp.{{ schema_fields_capitalize[0] | lower }} ==  ref{{ schema_fields_capitalize[0] }}.current.value ) {
            window.location.href = "/{{ entity_lower }}/list"
        } else {
            alert(resp.response.data.detail)
        }
    }
    const submitHandler = async (e) => {
        e.preventDefault()

        if (id) {
            const r = await update{{ entity }}(id, {% for field in schema_fields_capitalize %}ref{{field}}.current.value, {% endfor %})
            setResp(r)
        } else {
            const r = await create{{ entity }}({% for field in schema_fields_capitalize %}ref{{field}}.current.value, {% endfor %})
            setResp(r)
        }
    }
    React.useEffect(()=> {
        if ({% for field in schema_fields %}{{field}}||{% endfor %}true) {
            {% for field in schema_fields_capitalize %}ref{{ field }}.current.value = {{ field | lower }}
            {% endfor %}
        }

    })
    return (
        <div className="max-w-sm mx-auto w-full px-4 py-8">
            <h1 className="text-3xl text-slate-800 dark:text-slate-100 font-bold mb-6">Ceating {{ entity }}</h1>
            <form onSubmit={submitHandler} method="POST">

                {% for field in schema_fields_capitalize %}<div>
                    <div>
                        <label className="block text-sm font-medium mb-1" htmlFor="{{ field }}-text">
                            {{ field }}
                        </label>
                        <input id="{{ field }}-text" className="form-input w-full" type="text" ref={ref{{ field }}}/>
                    </div>
                </div>

                {% endfor %}
                <div className="m-1.5">
                      <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
}

export default Form;