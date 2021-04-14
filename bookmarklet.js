(function() {
    function setButton() {
        Array.from(document.querySelectorAll(".content a:not([data-has-save-button]) > img")).forEach(v => {
            var a = document.createElement("button");
            a.textContent = "save URL";
            a.onclick = (evt) => {
                console.log(evt);
                const ref = location.href;
                const link = evt.target.parentElement.href;
                fetch(`https://cryptic-wildwood-50649.herokuapp.com/?referrer=${ref}&url=${link}&code=z`).then(r => r.json()).then(v => console.log(v));
                return false;
            };
            v.parentElement.dataset.hasSaveButton = true;
            v.parentElement.appendChild(a);
        })
    }
    setInterval(() => {setButton()}, 1000);
})();