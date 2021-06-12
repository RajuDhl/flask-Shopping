const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
let status_array = ["Repo"];

//function removeItemAll(arr, value) {
//    let i = 0;
//    console.log(arr);
//try {
//    while (i < arr.length) {
//        if (arr[i] === value) {
//            arr.splice(i, 1);
//       } else {
//           ++i;
//       }
//   }
//   return arr;
//}
function financial(value) {
    let absValue = Math.abs(value);
    let returnString = Number(absValue).toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    });
    return value < 0 ? '(' + returnString + ')' : returnString;
}
//function update_filters(elem) {
//    console.log(elem);
//    status_array = [];
//    const group = Array(document.getElementsByClassName('filter'));
//console.log(group);
//    group.forEach(function(){
//        console.log(this);
//x.classList = removeItemAll(x.classList, 'active');
//    });
//    status_array.push(elem);
//    document.getElementById(elem).classList.add('active');
//    refresh_data();
//    console.log(status_array);
//}
//console.log(list);
queryKey = {
    'Repo':{'query':'gaap_date', 'display': 'Repo (GAAP)  Date '},
    'OCO':{'query':'gaap_date', 'display': 'Repo (GAAP)  Date '},
    'Sold':{'query':'date_sold', 'display': 'Date Sold'},
    'Reinstate':{'query':'gaap_date', 'display': 'Repo (GAAP)  Date '}
}
function updateFilter(target){
    console.log("the target ", target);
    const btnContainer = document.getElementById("filter-group");
    let btns = btnContainer.getElementsByClassName("btn");
    for (let i = 0; i < btns.length; i++) {
        btns[i].classList.remove("active");
    }
    document.getElementById(target).classList.add('active');
    status_array = [target];
    console.log('status array ', status_array);
    document.getElementById('query-key').innerHTML = queryKey[status_array[0]]['display'];
    //console.log(status_array);
    refresh_data(status_array[0]);
}



//function filterSelection(target) {
//  document.querySelectorAll('.filterDiv').forEach((div) => {
//    if (target === 'all' || div.classList.contains(target)) {
//      div.classList.remove('hide');
//    } else {
//      div.classList.add('hide');
//    }
//  });
//}
const accountingView = {
    'loan':{'type':'numeric', 'display':'Loan'},
    'status':{'type':'alpha', 'display':'Loan'},
    'repo_category':{'type':'alpha', 'display':'Repo Category'},
    'gaap_date':{'type':'date', 'display':'GAAP Date'},
    'noi_sent':{'type': 'date', 'display':'NOI Sent'},
    'dafs':{'type': 'date', 'display':'DAFS'},
    'date_sold':{'type':'date', 'display':'Date Sold'},
    'co_date':{'type':'date', 'display':'CO Date'},
    'months_in_inventory':{'type':'numeric', 'display':'Months in inventory'},
    'location':{'type':'alpha', 'display':'Location'},
    'balance_repo_date':{'type':'numeric', 'display':'Balance Repo Date'},
    'cr_grade':{'type':'numeric', 'display':'CR Grade'},
    'chargeable_damages':{'type':'numeric', 'display':'Chargeable Damages'},
    'awv':{'type': 'numeric', 'display': 'AWV'},
    'mmr':{'type':'numeric', 'display': 'MMR'},
    'cash_price':{'type':'numeric', 'display':'Cash Price'},
    'estimated_recovery':{'type':'numeric', 'display':'Estimated Recovery'},
    'current_mo_proceeds_estimate':{'type':'numeric', 'display':'Current Month Proceeds'},
    'eom_gaap_proceeds_estimate':{'type':'numeric', 'display':'EOM GAAP Proceeds'},
    'actual_proceeds':{'type':'numeric', 'display':'Actual Proceeds'},
    'back_end_product_cancellation':{'type':'numeric', 'display':'Back End Cancellations'},
    'insurance_claims':{'type':'numeric', 'display':'Insurance Claims'},
    'gross_co_amt':{'type':'numeric', 'display':'Gross CO Amount'},
    'unearned_discount':{'type':'numeric', 'display':'Unearned Discount'},
    'net_loss_or_gain':{'type':'numeric', 'display':'Net Loss or Gain'},
    'recovery':{'type':'numeric', 'display':'Recovery'},
    'rem_bal':{'type':'numeric', 'display':'Remaining Balance'},
    'cash_or_new_ac':{'type':'alpha', 'display':'Cash or New AC'},
    'acct_min_val':{'type':'numeric', 'display':'Min Value'},
    'acct_gain_loss':{'type':'numeric', 'display':'Gain / Loss'},
    'acct_diff':{'type':'numeric', 'display':'Difference'},
    'acct_repo_month':{'type':'alpha', 'display':'Repo Month'},
    'repo_allow2_hist':{'type':'numeric', 'display':'Allow2'},
    'pforma_nrv':{'type':'numeric', 'display':'Proforma NRV'},
    'pforma_gain_loss':{'type':'numeric', 'display':'Proforma Gain / Loss'},
    'pforma_diff':{'type':'numeric', 'display':'Proforma Difference'}
};

function createHeaders(view){
    const table = document.getElementById('repo-log');
    const header = table.createTHead();
    header.className = 'thead-light';
    const row = header.insertRow(0);
    for (let [key, value] of Object.entries(view)) {
        let cell = document.createElement('th');
        cell.setAttribute('data-sortable-type', value['type']);
        cell.innerHTML = value['display'];
        row.append(cell);
    }
}

function createRow(obj, view){

    const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
    console.log()
    let newRow   = tableRef.insertRow();
    view.forEach(function(column){
        let newCell  = newRow.insertCell();
        newCell.id = column;
        if (['gaap_date', 'noi_sent', 'dafs', 'date_sold', 'co_date'].includes(column)) {
            if(obj[column] !== null && obj[column] !== undefined) {
                // console.log("date up ===> ", obj[column], column)
                try {
                    let date = new Date(obj[column]).toLocaleDateString();
                    newCell.innerHTML = date;
                    newCell.setAttribute('data-sortable-type', 'date');
                    newCell.setAttribute('data-sortable-value', date);
                } catch (err) {
                    newCell.innerHTML = null;
                }
            }
            else {
                newCell.innerHTML = null;
            }
        } else if(column === 'loan'){
            // console.log("loan ====> ", obj[column])
            newCell.innerHTML = '<a href="/repo/'+parseFloat(obj[column]).toFixed(1)+'">'+parseFloat(obj[column]).toFixed(1)+'</a>';
            newCell.style.textAlign = "right";

        } else if (typeof obj[column] === 'number') {
            newCell.innerHTML = financial(obj[column]);
            newCell.style.textAlign = "right";
            newCell.setAttribute('data-sortable-type', 'numeric');
            newCell.setAttribute('data-sortable-value', obj[column]);
            if (['months_in_inventory', 'cr_grade'].includes(column)) {
                newCell.innerHTML = obj[column].toFixed(1);
                newCell.setAttribute('data-value', obj[column].toFixed(1));
                // display as number not money.
            } else if (['estimated_recovery', 'acct_diff', 'pforma_diff', 'repo_allow2_hist'].includes(column)) {
                // display as percentages
                newCell.innerHTML = String((obj[column]*100).toFixed(1))+'%';
                newCell.setAttribute('data-value', obj[column]*100);
            }
        } else{
            console.log("else case ===> ", obj[column])
            newCell.innerHTML = obj[column] || null;
            newCell.style.textAlign = "center";
            if (typeof obj[column] === 'string') {
                newCell.innerHTML = obj[column].toUpperCase() || null;
            }
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
        if (['gaap_date', 'noi_sent', 'dafs', 'date_sold', 'co_date'].includes(column)) {
            try {
                let date = obj[column].toDate();
                newCell.innerHTML =  String(date.getMonth()+1)+'/'+String(date.getDate())+'/'+String(date.getFullYear());
                newCell.setAttribute('data-sortable-type', 'date');
                newCell.setAttribute('data-sortable-value', date);
            } catch (err) {
                newCell.innerHTML = null;
            }
        } else if(column === 'loan'){
            newCell.innerHTML = '<a href="/repo/'+obj[column].toFixed(1)+'">'+obj[column].toFixed(1)+'</a>';
            newCell.style.textAlign = "right";

        } else if (typeof obj[column] === 'number') {
            newCell.innerHTML = financial(obj[column]);
            newCell.style.textAlign = "right";
            newCell.setAttribute('data-sortable-type', 'numeric');
            newCell.setAttribute('data-sortable-value', obj[column]);
            if (['months_in_inventory', 'cr_grade'].includes(column)) {
                newCell.innerHTML = obj[column].toFixed(1);
                newCell.setAttribute('data-value', obj[column].toFixed(1));
                // display as number not money.
            } else if (['estimated_recovery', 'acct_diff', 'pforma_diff', 'repo_allow2_hist'].includes(column)) {
                // display as percentages
                newCell.innerHTML = String((obj[column]*100).toFixed(1))+'%';
                newCell.setAttribute('data-value', obj[column]*100);
            }
        } else{
            newCell.innerHTML = obj[column] || null;
            newCell.style.textAlign = "center";
            if (typeof obj[column] === 'string') {
                newCell.innerHTML = obj[column].toUpperCase() || null;
            }
        }
    });
}

let st = new Date(new Date().setFullYear(new Date().getFullYear() - 1));
let dt = new Date();
let stm = new Date(new Date().setMonth(new Date().getMonth() - 1));

function set_timePeriod(){
    tableRef.innerHTML = '';
    let start = new Date(document.getElementById('start-date').value)
    let end = new Date(document.getElementById('end-date').value + ' 23:59')
    timePeriod = start.getTime();
    until = end.getTime();
    let loan_amount = document.getElementById('search_loan').value

    $.ajax({
        url: `/api/repo-log?status=${status_array[0]}&start=${timePeriod}&until=${until}&loan=${loan_amount}`,
        success: function(data) {
            let docs = data
            docs.forEach( function (doc){
                // console.log("data is =====>", doc)
                // let CN = new Date(doc.gaap_date).getTime()
                // if(CN <= until && CN >= timePeriod){
                createRow( doc, Object.keys(accountingView))
                // }
                 updateHeaderDisplay(data);
            })
        }
    });
    // refresh_data(status_array[0]);
}


const user_email = document.getElementById("user_email").value
const user_password = document.getElementById("user_password").value

function displayDate(date){
    const dateTimeFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'numeric', day: 'numeric' })
    const [{ value: month },,{ value: day },,{ value: year }] = dateTimeFormat .formatToParts(date )
    return(`${month}/${day}/${year }`);

}

function updateHeaderDisplay(snapshot){

    let total = [];
    let losses = []

    if (status_array[0] === 'Repo') {
        snapshot.forEach(function (doc) {
            total.push(doc['balance_repo_date']);
            // console.log("date and gaap date",new Date(doc['gaap_date']).getMonth(), new Date().getMonth())
            if (doc['gaap_date'] !== new Date().getMonth() + 1) {
                losses.push(doc['eom_gaap_proceeds_estimate']);
            }
        });
        // console.log("status array is repo", losses);
        /*if (until.getMonth() === new Date().getMonth()) {*/
        document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.length + '<br/>Total: '
            + financial(total.reduce((a, b) => a + b, 0)) + '<br/>Total estimated losses: '
            + financial(losses.reduce((a, b) => a + b, 0))+ '*' + ' &nbsp; <i>(EOM GAAP Proceeds)</i><br/>Estimated average loss: '
            + financial(losses.reduce((a, b) => a + b, 0) / losses.length);
        /*} else {
            document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.length + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0)) + '<br/>Total estimated losses: ' + financial(losses.reduce((a, b) => a + b, 0)) + ' &nbsp; <i>(EOM GAAP Proceeds)</i><br/>Estimated average loss: ' + financial(losses.reduce((a, b) => a + b, 0) / losses.length);
        }*/

    } else if (status_array[0] === 'OCO') {
        snapshot.forEach(function (doc) {
            total.push(doc['balance_repo_date']);
            losses.push(doc['balance_repo_date'] - doc['actual_proceeds'] - doc["unearned_discount"]);
        });
        document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.length
            + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0))
            + '<br/>Total losses: '
            + financial(losses.reduce((a, b) => a + b, 0))
            + '<br/>Average loss: '
            + financial(losses.reduce((a, b) => a + b, 0)/losses.length);
    } else if (status_array[0] === 'Sold') {
        snapshot.forEach(function (doc) {
            total.push(doc['balance_repo_date']);
            if (doc['date_sold'] !== new Date().getMonth() + 1) {
                //(balance  at repo date) - actual proceeds + unearned_discount
                losses.push(doc['balance_repo_date'] - doc['actual_proceeds'] - doc['unearned_discount'] );
            } else{
                losses.push(doc['actual_proceeds'] - doc['eom_gaap_proceeds_estimate'] );
            }
        });
        document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.length
            + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0))
            + '<br/>Total losses: ' + financial(losses.reduce((a, b) => a + b, 0))
            + ' &nbsp; <br/>Average loss: ' + financial(losses.reduce((a, b) => a + b, 0) / losses.length);
    }
    else if (status_array[0] === 'Reinstate'){
        snapshot.forEach(function (doc) {
                    total.push(doc['balance_repo_date']);
                    losses.push(doc['balance_repo_date'] - doc['actual_proceeds'] - doc["unearned_discount"]);
                });
         document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.length
            + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0))
            + '<br/>Total losses: '
            + financial(losses.reduce((a, b) => a + b, 0))
            + '<br/>Average loss: '
            + financial(losses.reduce((a, b) => a + b, 0)/losses.length);
    }
}

function refresh_data(status) {
    tableRef.innerHTML = '';
    set_timePeriod()
     // const xhr = new XMLHttpRequest();
    // if (xhr.status === 200){
    //    set_timePeriod()
    // }
    // const xhr = new XMLHttpRequest();
    // xhr.onreadystatechange = function() {
    //     if (xhr.readyState === XMLHttpRequest.DONE) {
    //         if (xhr.status === 200) {
    //             const data = JSON.parse(xhr.responseText) // xhr.responseText
    //             data.forEach( function (doc) {
    //                 createRow(doc, Object.keys(accountingView))
    //             })
    //             updateHeaderDisplay(data);
    //         }
    //         else {
    //             console.log ('Error: ' + xhr.status);
    //         }
    //     }
    // };
    // xhr.open("GET", "/api/repo-log?status="+status, true)
    // xhr.send();

}
window.onload = function() {
    //lookBack('all');
    document.getElementById('start-date').max = new Date();
    let end = document.getElementById('end-date');
    let start = document.getElementById('start-date');
    end.max = new Date();
    start.min = st
    end.value = String(dt.getFullYear()) +'-'+ String("0" + (dt.getMonth() + 1)).slice(-2) +'-'+ String("0" + String((parseInt(dt.getDate()))) ).slice(-2);
    start.value = String(st.getFullYear()) +'-'+ String("0" + (dt.getMonth() + 1)).slice(-2) +'-'+ String("0" + String((parseInt(dt.getDate()))) ).slice(-2);
    set_timePeriod()

}
function filter_loan(){
    tableRef.innerHTML = '';
    loan_amount = document.getElementById('search_loan').value
    console.log("loan amount is", loan_amount)
    display_loan_filter();
}
function display_loan_filter(){
    console.log(typeof(parseFloat(loan_amount)))
    console.log("page status is", status_array[0])
    if (loan_amount!== ""){
        let loan = parseFloat(loan_amount)
    $.ajax({
        url: `/api/repo-log?status=${status_array[0]}&loan=${loan_amount}`,
        success: function(data) {
            let docs = data
            docs.forEach( function (doc){
                    createRow( doc, Object.keys(accountingView))
            })
            // just to reset the search value as it is in current appspot version
            document.getElementById('search_loan').value = ""
        }
    });
    }else{
        var repo = document.getElementById("repo-log")
        repo.style.display='block';
        location.reload("forceGet")
        //refresh_data()
    }
}