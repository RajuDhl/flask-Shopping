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
    'Sold':{'query':'date_sold', 'display': 'Date Sold'}
}
function updateFilter(target){
    const btnContainer = document.getElementById("filter-group");
    let btns = btnContainer.getElementsByClassName("btn");
    for (let i = 0; i < btns.length; i++) {
        btns[i].classList.remove("active");
    }
    document.getElementById(target).classList.add('active');
    status_array = [target];
    document.getElementById('query-key').innerHTML = queryKey[status_array[0]]['display'];
    console.log(status_array);
    refresh_data();
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
    let newRow   = tableRef.insertRow();
    view.forEach(function(column){
        let newCell  = newRow.insertCell();
        newCell.id = column;
        if (['gaap_date', 'noi_sent', 'dafs', 'date_sold', 'co_date'].includes(column)) {
            try {
                let date = obj[column].toDate();
                newCell.innerHTML = String(date.getMonth()+1)+'/'+String(date.getDate())+'/'+String(date.getFullYear());
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
let timePeriod = new Date(new Date(2020, 2, 1).toLocaleString('en-US', {'timeZone':'America/Chicago'}));
//let until = new Date(new Date().toLocaleString('en-US', {'timeZone':'America/Chicago'}))
let until = document.getElementById('end-date').value;

function set_timePeriod(){
    timePeriod = new Date(document.getElementById('start-date').value);
    until = new Date(document.getElementById('end-date').value);
    refresh_data();
}

firebase.initializeApp({
    apiKey: 'AIzaSyAH5YeDx_VLm_gFhXiXAQXG9fzr8Oigzpg',
    authDomain: 'same-day-auto',
    projectId: 'same-day-auto',
    databaseURL: ' https://same-day-auto.firebaseio.com/',
    storageBucket: "same-day-auto.appspot.com"
});

const db = firebase.firestore();

function displayDate(date){
    const dateTimeFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'numeric', day: 'numeric' })
    const [{ value: month },,{ value: day },,{ value: year }] = dateTimeFormat .formatToParts(date )
    return(`${month}/${day}/${year }`);

}

function updateHeaderDisplay(snapshot){
    console.log('update header display for '+status_array[0]);
    let total = [];
    let losses = []

    if (status_array[0] === 'Repo') {
        snapshot.forEach(function (doc) {
            total.push(doc.data()['balance_repo_date']);
            if (doc.data()['gaap_date'] !== new Date().getMonth() + 1) {
                losses.push(doc.data()['eom_gaap_proceeds_estimate']);
            }
        });
        if (until.getMonth() === new Date().getMonth()) {
            document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.size + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0)) + '<br/>Total estimated losses: ' + financial(losses.reduce((a, b) => a + b, 0))+ '*' + ' &nbsp; <i>(EOM GAAP Proceeds)</i><br/>Estimated average loss: ' + financial(losses.reduce((a, b) => a + b, 0) / losses.length)+ '*  &nbsp; *Does not include current month repos';
        } else {
            document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.size + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0)) + '<br/>Total estimated losses: ' + financial(losses.reduce((a, b) => a + b, 0)) + ' &nbsp; <i>(EOM GAAP Proceeds)</i><br/>Estimated average loss: ' + financial(losses.reduce((a, b) => a + b, 0) / losses.length);
        }

    } else if (status_array[0] === 'OCO') {
        console.log('got here');
        snapshot.forEach(function (doc) {
            total.push(doc.data()['balance_repo_date']);
            losses.push(doc.data()['balance_repo_date'] - doc.data()['actual_proceeds'] - doc.data()["unearned_discount"]);
        });
        document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.size + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0)) + '<br/>Total losses: ' + financial(losses.reduce((a, b) => a + b, 0)) + '<br/>Average loss: ' + financial(losses.reduce((a, b) => a + b, 0)/losses.length);
    } else if (status_array[0] === 'Sold') {
        snapshot.forEach(function (doc) {
            total.push(doc.data()['balance_repo_date']);
            if (doc.data()['date_sold'] !== new Date().getMonth() + 1) {
                //(balance  at repo date) - actual proceeds + unearned_discount
                losses.push(doc.data()['balance_repo_date'] - doc.data()['actual_proceeds'] - doc.data()['unearned_discount'] );
            } else{
                losses.push(doc.data()['actual_proceeds'] - doc.data()['eom_gaap_proceeds_estimate'] );
            }
        });
        document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.size + '<br/>Total: ' + financial(total.reduce((a, b) => a + b, 0)) + '<br/>Total losses: ' + financial(losses.reduce((a, b) => a + b, 0)) + ' &nbsp; <br/>Average loss: ' + financial(losses.reduce((a, b) => a + b, 0) / losses.length);

    }

}

function refresh_data() {
    tableRef.innerHTML = '';
    db.collection("repos")
        .where("status", "==", status_array[0])
        .where(queryKey[status_array[0]]['query'], "<=", until) // end date (most recent)
        .where(queryKey[status_array[0]]['query'], ">=", timePeriod) // start date
        .orderBy(queryKey[status_array[0]]['query'], "desc")
        .get()
        .then(function (querySnapshot) {
            querySnapshot.forEach(function (doc) {
                createRow(doc.data(), Object.keys(accountingView));
            });
            updateHeaderDisplay(querySnapshot);
            //document.getElementById('alert-light').innerHTML = 'count: ' + querySnapshot.size;
        })
        .catch(function (error) {
            console.log("Error getting documents: ", error);
        });

}
window.onload = function() {
    //lookBack('all');
    document.getElementById('start-date').max = new Date();
    let end = document.getElementById('end-date');
    end.max = new Date();
    let dt = new Date();
    end.value = String(dt.getFullYear()) +'-'+ String("0" + (dt.getMonth() + 1)).slice(-2) +'-'+ String("0" + dt.getDate()).slice(-2);
    set_timePeriod()
}