const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
window.onload= function(){refresh_data()};
function createRow(obj,view){
    const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];

    let newRow   = tableRef.insertRow();
    view.forEach(function(column){
        let newCell  = newRow.insertCell();
        newCell.id = column;
        // console.log("column ", column );
        if (column==='extension'){
            newCell.innerHTML = '<a href="/extension-form-letter/'+obj["customer_number"]+'" style="target:blank;">Download</a>';
            newCell.style.textAlign = "left";
        }
        if(column === 'customer_number'){
            try{
                newCell.innerHTML = '<a href="/extension/'+obj[column]+'">'+obj[column]+'</a>';
                newCell.style.textAlign = "left";
            }catch (err){
                newCell.innerHTML = null;
            }
        }
        if (["requested_date","approved_date","prior_due_date","new_due_date","prior_maturity_date","new_maturity_date"].includes(column)){
            try{
               let date = new Date(obj[column]).toLocaleDateString();
                newCell.innerHTML = date;
                newCell.setAttribute('data-sortable-type', 'date');
                newCell.setAttribute('data-sortable-value', date);
            } catch (err) {
                newCell.innerHTML = null;
            }
        }
        if (["account_number","final_status","approved_by","extension_type","collector"].includes(column)){
            let data = obj[column]
            // console.log("data", data);
            newCell.innerHTML = data
        }

    });
}
function createRowNew(obj, view){

    const tableRef = document.getElementById("log_filter").getElementsByTagName('tbody')[0];
    console.log()
    let newRow   = tableRef.insertRow();
    view.forEach(function(column){
        let newCell  = newRow.insertCell();
        newCell.id = column;
        if (column==='extension'){
            newCell.innerHTML = '<a href="/extension-form-letter/'+obj["CUST_NUMBER"]+'" style="target:blank;">Download</a>';
            newCell.style.textAlign = "left";
        }
        if(column === 'CUST_NUMBER'){
            try{

                newCell.innerHTML = '<a href="/extension/'+obj['id']+'">'+obj[column]+'</a>';
                newCell.style.textAlign = "left";
            }catch (err){
                newCell.innerHTML = null;
            }
        }
        if (["requested_date","approved_date","prior_due_date","new_due_date","prior_maturity_date","new_maturity_date"].includes(column)){
            try{
                let date = new Date(obj[column]).toLocaleDateString();
                newCell.innerHTML = date;
                newCell.setAttribute('data-sortable-type', 'date');
                newCell.setAttribute('data-sortable-value', date);
            } catch (err) {
                newCell.innerHTML = null;
            }
        }
        if (["ACCOUNT_NUMBER","FinalStatus","ApprovedBy","ExtensionType","Collector"].includes(column)){
            let data = obj[column]
            newCell.innerHTML = data
        }
    });
}
const accountingView = {
    "extension":{"type":"numeric","display":"Extension"},
    "customer_number":{"type":"numeric","display":"Customer Number"},
    "account_number":{"type":"numeric","display":"Account Number"},
    "requested_date":{"type":"date","display":"Requested Date"},
    "final_status":{"type":"string","display":"Final Status"},
    "approved_date":{"type":"date","display":"Approved Date"},
    "approved_by":{"type":"string","display":"Approved By"},
    "extension_type":{"type":"string","display":"Extension Type"},
    "collector":{"type":"string","display":"Collector"},
    "prior_due_date":{"type":"date","display":"Prior Due Date"},
    "new_due_date":{"type":"date","display":"New Due Date"},
    "prior_maturity_date":{"type":"date","display":"Prior Maturity Date"},
    "new_maturity_date":{"type":"date","display":"New Maturity Date"}

}
function count_extension(snapshot){
    document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.length
    console.log("length is", snapshot.length)
}
function refresh_data() {
    tableRef.innerHTML = '';
    var repo_filer =document.getElementById('log_filter')
    repo_filer.style.display='none'
    var repo = document.getElementById("repo-log")
    repo.style.display='block';
    /*db.collection("extension").orderBy("RequestedDate","desc")
        .get()
        .then(function (querySnapshot) {
            querySnapshot.forEach(function (doc) {
                var value=doc.data()
                value["id"]=doc.id
                console.log
                createRow(value,Object.keys(accountingView));
            });
            count_extension(querySnapshot)
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
                count_extension(data)
            }
            else {
                console.log ('Error: ' + xhr.status);
            }
        }
    };
    xhr.open("GET", "/api/extension-log", true)
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
        url: "/api/extension-log",
        success: function(data) {
            let docs = data
            docs.forEach( function (doc){
                let CN = parseFloat(doc.customer_number)
                if(loan === CN){
                    createRow( doc, Object.keys(accountingView))
                }
                count_extension(data)
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