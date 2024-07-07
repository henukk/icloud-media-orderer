import streamlit as st
import streamlit.components.v1 as components

def toggle_extension(ext):
    if ext in st.session_state.selected_extensions:
        st.session_state.selected_extensions.remove(ext)
    else:
        st.session_state.selected_extensions.append(ext)

def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}'
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)
