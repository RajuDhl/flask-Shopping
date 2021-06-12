function changeUser(userID, url) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4)
        location.reload();
    }
    xhr.open("GET", url + userID, true);
    xhr.send();
}