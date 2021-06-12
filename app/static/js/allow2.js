const output = document.getElementById('output');

function refresh_data(months, columns) {
    output.innerHTML = "";
    const s = document.createElement("span");
    s.id = "counter";
    output.append(s);

    const tableRef = document.createElement("table");
    tableRef.className = "table";
    tableRef.classList.add("table-sm");
    const header = tableRef.createTHead()
    let row = header.insertRow(0);
    let h;
    if (columns.includes('pforma_diff')){
        h = ['Loan #', 'Status', 'Date Sold', 'PF NRV', 'PF Gain Loss', 'PF Diff' ].reverse();

    } else{
        h = ['Loan', 'Status', 'Date Sold', 'Min Value', 'Gain Loss', 'Diff'].reverse();
    }

    h.forEach(function(col){
        let cell = row.insertCell(0);
        cell.innerHTML = col;
        cell.style.textAlign = 'right';
    });

    output.append(tableRef);

    console.log('months ===> ', months)

    /*db.collection('repos')
        .where("status", "==", "Sold")
        .where("acct_sold_month", "in", months)
        //.where("date_sold", "<=", endDate) // end date (most recent)
        //.where("date_sold", ">=", startDate) // start date
        .orderBy("loan", "desc")
        .get()
        .then(function (querySnapshot) {
            //console.log(querySnapshot.size)
            document.getElementById('counter').innerHTML = 'Unit count: ' + String(querySnapshot.size);
            querySnapshot.forEach(function(doc) {
                createRow(doc.data(), columns, tableRef);
            });
        })
        .catch(function (error) {
            console.log("Error getting documents: ", error);
        });*/
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText) // xhr.responseText
                document.getElementById('counter').innerHTML = 'Unit count: ' + String(data.length);
                data.forEach( function (doc) {
                    // refresh_data(doc['months'], view);
                    createRow(doc, columns, tableRef);
                })
            }
            else {
                console.log ('Error: ' + xhr.status);
            }
        }
    };
    const params = `months=${months}`
    xhr.open("GET", `/api/nrv2?`+params, true)
    xhr.send(params);


}

function unitLookUp(elem){
    console.log(elem);
    const views = {
        'val_allow': ['loan', 'status', 'date_sold', 'pforma_nrv', 'pforma_gain_loss', 'pforma_diff' ],
        'real_disc_to_nrv': ['loan', 'status', 'date_sold', 'acct_min_val', 'acct_gain_loss', 'acct_diff']
    };
    let m = elem.split('@')[1];
    let t = elem.split('@')[0];
    console.log(m,"===", t)
    //console.log('t: '+ t, []views[t]);
    let view = views[t];
    /*let db_ref = db.collection(t).doc(m);
    db_ref.get().then(function(doc) {
        //console.log(doc.data())
        //console.log(doc.data()['months'], doc.data()['end'], doc.data()['start'], view);
        refresh_data(doc.data()['months'], view);
    });*/
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText) // xhr.responseText
                data.forEach( function (doc) {
                    refresh_data(doc['months'], view);
                })
            }
            else {
                console.log ('Error: ' + xhr.status);
            }
        }
    };
    xhr.open("GET", `/api/nrv?code=${m}`, true)
    xhr.send();
}

function financial(value) {
    if (value && value !== '') {
        let absValue = Math.abs(value);
        let returnString = Number(absValue).toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        });
        return value < 0 ? '(' + returnString + ')' : returnString;
    } else{
        return "0";
    }
}


function createRow(obj, view, table){
    let newRow = table.insertRow();
    view.forEach(function(column) {

        let newCell = newRow.insertCell();
        if (['status'].includes(column)) {
            newCell.innerHTML = obj[column];
            newCell.style.textAlign = "center";
        } else if (['loan'].includes(column)) {
            newCell.innerHTML = '<a href="/repo/'+String(obj[column])+'">'+obj[column]+'</a>';

        } else if (['pforma_diff', 'acct_diff'].includes(column)) {
            newCell.innerHTML = String((obj[column] * 100).toFixed(1))+'%';

        } else if(['date_sold'].includes(column)) {
            // let dt = obj[column].toDate();
            let dt = new Date( obj[column]);

            newCell.innerHTML = String(dt.getMonth()+1)+'/'+String(dt.getDate())+'/'+String(dt.getFullYear());
        } 

        else{
            let d = obj[column];
            if (d === 0){
                newCell.innerHTML = (obj[column]);
            }
            else{
                newCell.innerHTML = financial(obj[column]);
            }
            
        }

        newCell.style.fontSize = '0.8em;'
        newCell.style.textAlign = "right";
    });

}