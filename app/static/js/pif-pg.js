function deleteMe() {
    let customer_number = document.getElementById('customer_number').value;
    let r = confirm("Are you sure you want to delete " + customer_number + "?");
    if (r) {

        let data = {'customer_number': customer_number}
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/delete-pif', false);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.send(JSON.stringify(data));
        let msg = 'Deleted '+customer_number;
        location.replace(window.location.pathname = "/pif-log?msg="+msg)
    }
}