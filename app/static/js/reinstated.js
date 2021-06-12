function financial(value) {
    let absValue = Math.abs(value);
    let returnString = Number(absValue).toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    });
    return value < 0 ? '(' + returnString + ')' : returnString;
}

window.onload = function (){
    const arr = document.getElementsByClassName('fin');
        for (let i = 0; i < arr.length; i++) {
            console.log(arr[i])
            arr[i].innerHTML = financial(arr[i].innerHTML);
        }
}