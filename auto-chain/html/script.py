script = """<script>
let doc = window.parent.document
doc.querySelector("[srcdoc]").style.display = 'none'

const parentElement = doc.querySelector(".main");

parentElement.addEventListener("click", function(event) {
console.log(event.target.innerText)
if (event.target.innerText=='👎') {
    
    let message = event.target.closest(".stChatMessage")
    console.log(message.style.backgroundColor)
    if(message.style.backgroundColor == 'rgba(255, 75, 75, 0.4)')
        message.style.backgroundColor = 'white'
    else if(message.style.backgroundColor == 'white')
        message.style.backgroundColor = 'rgba(255, 75, 75, 0.4)'
    else
        message.style.backgroundColor = 'rgba(255, 75, 75, 0.4)'
    console.log(message.style.backgroundColor)
}
});

let messages = doc.querySelectorAll(".stChatMessage")
for (var i=0;i<messages.length;i++){
        message = messages[i]
        console.log(message.querySelector('[kind="primary"]'))
        if(i%2!=0){
            primary = message.querySelector('[kind="primary"]')
            secondary = message.querySelector('[kind="secondary"]')
            if(primary && primary.innerText == '👎')
                message.style.backgroundColor = 'rgba(255, 75, 75, 0.4)'
            else if(secondary && secondary.innerText == '👎')
                message.style.backgroundColor = 'white'
        }
    
}
console.log(messages)
</script>"""