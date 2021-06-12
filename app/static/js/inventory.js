function financial(value) {
    let absValue = Math.abs(value);
    let returnString = Number(absValue).toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    });
    return value < 0 ? '(' + returnString + ')' : returnString;
}
const count = document.getElementById('repoCount').innerHTML;
document.getElementById('avgGross').innerHTML = financial(parseFloat(document.getElementById('gross').innerHTML)/count);
document.getElementById('gross').innerHTML = financial(document.getElementById('gross').innerHTML);


document.getElementById('avgAllow').innerHTML = financial(parseFloat(document.getElementById('allow').innerHTML)/count)
document.getElementById('allow').innerHTML = financial(document.getElementById('allow').innerHTML);

document.getElementById('avgNet').innerHTML = financial(parseFloat(document.getElementById('net').innerHTML)/count)
document.getElementById('net').innerHTML = financial(document.getElementById('net').innerHTML);

let losses = document.getElementsByClassName('loss');
for (let i = 0; i < losses.length; i++) {
losses[i].innerHTML = financial(losses[i].innerHTML);
}

document.getElementById('asof').innerText = String(new Date().getMonth()+1) + '/' + String(new Date().getDate()) + '/' + String(new Date().getFullYear());
//document.getElementById('repo_loss').innerHTML = financial(document.getElementById('repo_loss').innerHTML);
//document.getElementById('sold_loss').innerHTML = financial(document.getElementById('sold_loss').innerHTML);
//document.getElementById('total_loss').innerHTML = financial(document.getElementById('total_loss').innerHTML);