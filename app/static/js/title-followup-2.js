const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
window.onload= function(){refresh_data()};
function createRow(obj,view){
    const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0]; 
    let newRow   = tableRef.insertRow();
    view.forEach(function(column){
        let newCell  = newRow.insertCell();
        newCell.id = column;
        if(column === "customer_number"){
            newCell.innerHTML = '<a href="/follow-up/'+obj[column]+'">'+obj[column]+'</a>';
            newCell.style.textAlign = "left";
        }
        if (["app_received","contract_date","title_due","white_slip_received","title_received"].includes(column)){
            try{
                if (obj[column] == null) {
                      // console.log("date for ", column ,"is ", obj[column])
                      newCell.innerHTML = null
                  }
                else {
                    let date = new Date(obj[column]).toLocaleDateString();
                    newCell.innerHTML = date;
                    newCell.setAttribute('data-sortable-type', 'date');
                    newCell.setAttribute('data-sortable-value', date);
                }
            }catch(err){
                newCell.innerHTML =null
            }
        }

        if (["account"].includes(column)){
            let data = obj[column]
            if (data){ newCell.innerHTML = data }

            
        }
        if (["dealer","name","follow_up_comments"].includes(column)){
            let data = obj[column]
            newCell.innerHTML = data
        }

    });
}
function createRowNew(obj, view){
    const tableRef = document.getElementById("log_filter").getElementsByTagName('tbody')[0];
    let newRow   = tableRef.insertRow();
    view.forEach(function(column){
        let newCell  = newRow.insertCell();
        newCell.id = column;
        if(column === "customer_number"){
            newCell.innerHTML = '<a href="/follow-up/'+obj[column]+'">'+obj[column]+'</a>';
            newCell.style.textAlign = "left";
        }
        if (["app_received","contract_date","title_due","white_slip_received","title_received"].includes(column)){
            try{
                let date = obj[column].toDate();
                newCell.innerHTML = String(date.getMonth()+1)+'/'+String(date.getDate())+'/'+String(date.getFullYear());
                newCell.setAttribute('data-sortable-type', 'date');
                newCell.setAttribute('data-sortable-value', date);
            }catch(err){
                newCell.innerHTML =null
            }
        }
        if (["account"].includes(column)){
            let data = obj[column]
            if (data){ newCell.innerHTML = data }   
        }
        if (["dealer","name","follow_up_comments"].includes(column)){
            let data = obj[column]
            newCell.innerHTML = data
        }

    });

}
const accountingView = {
    "customer_number":{"type":"numeric","display":"Customer Number"},
    "account":{"type":"numeric","display":"Account Number"},
    "dealer":{"type":"string","display":"Dealer"},
    "name":{"type":"string","display":"Name"},
    "app_received":{"type":"date","display":"App Received"},
    "contract_date":{"type":"date","display":"Contract Date"},
    "title_due":{"type":"date","display":"Tilte Due"},
    "white_slip_received":{"type":"date","display":"White Slip Received"},
    "title_received":{"type":"date","display":"Title Received"},
    "follow_up_comments":{"type":"string","display":"Follow Up Comments"},
}

function count_followup(querySnapshot){
    document.getElementById("alert-light").innerHTML = "Count :"+querySnapshot.length;
}

function refresh_data() {
    tableRef.innerHTML = '';
    const repo_filer =document.getElementById('log_filter')
    repo_filer.style.display='none'
    const repo = document.getElementById("repo-log")
    repo.style.display='block';
    /*db.collection("Title_FollowUp").where("app_received","==","").orderBy("contract_date","desc")
        .get()
        .then(function (querySnapshot) {
            querySnapshot.forEach(function (doc) {
                createRow(doc.data(),Object.keys(accountingView));
            });
            count_followup(querySnapshot)
        })
        .catch(function (error) {
            console.log("Error getting documents: ", error);
    });*/
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText) // xhr.responseText
                //alert(data);
                data.forEach( function (doc) {
                    createRow(doc, Object.keys(accountingView))
                })
                count_followup(data)
            }
            else {
                console.log ('Error: ' + xhr.status);
            }
        }
    };
    xhr.open("GET", "/api/title-follow-up", true)
    xhr.send();

}

function refresh_Historical_data() {
    tableRef.innerHTML = '';
    const btnContainer = document.getElementById("filter-group");
    let btns = btnContainer.getElementsByClassName("btn");
    for (let i = 0; i < btns.length; i++) {
        btns[i].classList.remove("active");
    }
    document.getElementById("Historical").classList.add('active');
    let timePeriod = new Date(new Date(2010,1,1).toLocaleString('en-US', {'timeZone':'America/Chicago'}));
    console.log(timePeriod)
    var repo_filer =document.getElementById('log_filter')
    repo_filer.style.display='none'
    var repo = document.getElementById("repo-log")
    repo.style.display='block';
    /*db.collection("Title_FollowUp").where("app_received",">",timePeriod).orderBy("app_received","desc")
        .get()
        .then(function (querySnapshot) {

            querySnapshot.forEach(function (doc) {
                console.log(doc.data()['app_received'])
                createRow(doc.data(),Object.keys(accountingView));
            });
            count_followup(querySnapshot)
        })
        .catch(function (error) {
            console.log("Error getting documents: ", error);
        });*/
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText) // xhr.responseText
                //alert(data);
                data.forEach( function (doc) {
                    createRow(doc, Object.keys(accountingView))
                })
                count_followup(data)
            }
            else {
                console.log ('Error: ' + xhr.status);
            }
        }
    };
    xhr.open("GET", "/api/title-follow-up?history=true", true)
    xhr.send();
}
function updateFilter(target){
    const btnContainer = document.getElementById("filter-group");
    let btns = btnContainer.getElementsByClassName("btn");
    for (let i = 0; i < btns.length; i++) {
        btns[i].classList.remove("active");
    }
    document.getElementById(target).classList.add('active');
    refresh_data();
}
function filter_loan(){
    tableRef.innerHTML = '';
    const repo_filer = document.getElementById('log_filter');
    repo_filer.style.display='none'
    const repo = document.getElementById("repo-log");
    repo.style.display='block';
    loan_amount = document.getElementById('search_loan').value
    display_loan_filter();
}
function display_loan_filter(){
    console.log(typeof(parseFloat(loan_amount)))
    if (loan_amount!== ""){
        let loan = parseFloat(loan_amount)
    $.ajax({
        url: "/api/title-follow-up",
        success: function(data) {
            let docs = data
            docs.forEach( function (doc){
                let CN = parseFloat(doc.customer_number)
                if(loan === CN){
                    createRow( doc, Object.keys(accountingView))
                }
            })
        }
    });
    }else{
        var repo = document.getElementById("repo-log")
        repo.style.display='block';
        location.reload("forceGet")
        //refresh_data()
    }
}