function financial(value) {
    let absValue = Math.abs(value);
    let returnString = Number(absValue).toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    });
    return value < 0 ? '(' + returnString + ')' : returnString;
}

document.getElementById('repoLoss').innerHTML = financial(document.getElementById('repoLoss').innerHTML);
document.getElementById('soldLoss').innerHTML = financial(document.getElementById('soldLoss').innerHTML);
document.getElementById('soldSameLoss').innerHTML = financial(document.getElementById('soldSameLoss').innerHTML);
document.getElementById('ocoLoss').innerHTML = financial(document.getElementById('ocoLoss').innerHTML);
document.getElementById('totalLoss').innerHTML = financial(document.getElementById('totalLoss').innerHTML);
document.getElementById('reinstates').innerHTML = financial(document.getElementById('reinstates').innerHTML);

const anchors = document.getElementsByClassName('lookback');

for (let i = 0; i < anchors.length; i++) {
    if (anchors[i].href === window.location.href) {
        anchors[i].style.color = 'gray';
    }
}

const nums = document.getElementsByClassName('fin');
for (let i = 0; i < nums.length; i++) {
    nums[i].innerHTML = financial(nums[i].innerHTML);
    nums[i].style.textAlign = 'right';

}
