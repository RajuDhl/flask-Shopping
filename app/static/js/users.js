var d = []
let options = [
    {text:"Repo Log", value:"Repo",hidden:false,disabled:false,selected:false},
    {text:"Extension Log",value:"Extension",hidden:false,disabled:false,selected:false},
    {text:"Title Follow-Up",value:"Title",hidden:false,disabled:false,selected:false},
    {text:"PIF Log",value:"Pif",hidden:false,disabled:false,selected:false}
]
function changeUser(userID,url) {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4)
            location.reload();
    }
    xhr.open("GET", url + userID, true);
    xhr.send();
}
function changeUserPermission(url) {
    //var uuid = document.getElementById("user_uuid").value
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4)
            location.reload();
    }
    const data = {};
    data['permission'] = options
    data['email'] = document.getElementById("user_email").value
    console.log(JSON.stringify(data))
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(data));
}
function test(details){
    var element=document.getElementById("permission")
    for (var i = 0; i < element.options.length; i++) {
        element.options[i].selected = "Extension Log";
    }
    //x[0].setAttribute("selected","")
    //console.log(x)
}

function set_permission(userID) {
    console.log("record", userID)
    ///api/getRoles
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if(xhr.status === 200 ) {
                const data = JSON.parse(xhr.responseText)

                // create options for bsMultiselect
                if(data['roles']){
                    data['roles'].forEach(function(obj) {
                        options.forEach(function (opt) {
                            if (opt.value === obj.name) {
                                opt.selected = true;
                            }
                        });
                    });
                }

                document.getElementById("user_management").style.display="none";
                document.getElementById("permission_management").style.display="block";
                document.getElementById("user_email").value= userID
                $("#permission").bsMultiSelect({
                    options : options
                });
            }
        }
    }
    xhr.open("GET", "/api/getRoles/" + userID, true);
    xhr.send();
}