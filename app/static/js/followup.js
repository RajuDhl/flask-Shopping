function deleteMe() {
    let account = document.getElementById('customer_number').value;
    let r = confirm("Are you sure you want to delete " + account + "?");
    if (r) {

        let data = {'customer_number': account}
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/delete-follow-up', false);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.send(JSON.stringify(data));
        let msg = 'Deleted '+account;
        location.replace(window.location.pathname = "/title-follow-up?msg="+msg)
    }
}