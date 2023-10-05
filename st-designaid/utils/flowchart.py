import streamlit as st
import streamlit.components.v1 as components


def mermaid(code: str) -> None:
    components.html(
        f"""
        <style>
            .mermaid-container {{
                width: 100%; /* or you can specify a fixed width like 800px */
                height: 600px; /* adjust as needed */
                overflow: auto; /* allows scrolling if the diagram is bigger than the specified size */
            }}
        </style>
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """, height=10000, width=1200
    )
