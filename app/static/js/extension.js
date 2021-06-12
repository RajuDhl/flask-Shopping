function deleteMe() {
    let cus_num = document.getElementById('repo_id').value;
    let r = confirm("Are you sure you want to delete " + cus_num + "?");
    if (r) {

        let data = {'cus_num': cus_num}
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/delete-extension', false);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.send(JSON.stringify(data));
        let msg = 'Deleted '+cus_num;
        location.replace(window.location.pathname = "/extension-log?msg="+msg)
    }
}