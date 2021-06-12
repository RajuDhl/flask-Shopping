
firebase.initializeApp({
    apiKey: "AIzaSyAH5YeDx_VLm_gFhXiXAQXG9fzr8Oigzpg",
    authDomain: "same-day-auto.firebaseapp.com",
    databaseURL: "https://same-day-auto.firebaseio.com",
    projectId: "same-day-auto",
    storageBucket: "same-day-auto.appspot.com",
    messagingSenderId: "96289819274",
    appId: "1:96289819274:web:72c778cc42dbe50bc27b73",
    measurementId: "G-1BP8PF81KJ"
    
           });
    const user_email = document.getElementById("user_email").value
    const user_password = document.getElementById("user_password").value
    const auth = firebase.auth()
    const signup = auth.signInWithEmailAndPassword(user_email,user_password)
    const db = firebase.firestore();
    
    const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
    window.onload= function(){refresh_data()};
    function createRow(obj,view){
        const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
        let newRow   = tableRef.insertRow();
        view.forEach(function(column){
            let newCell  = newRow.insertCell();
            newCell.id = column;
            if(column === "customer_number"){
                newCell.innerHTML = '<a href="/pif/'+obj[column]+'">'+obj[column]+'</a>';
                newCell.style.textAlign = "left";
            }
            if (["date_pif","op_sent","date_canceled","ttl-cntrct_recd","ttl-cntrct_sent",].includes(column)){
                try{
                    newCell.innerHTML = new Date(obj[column]).toLocaleDateString();
                    newCell.setAttribute('data-sortable-type', 'date');
                    newCell.setAttribute('data-sortable-value', date);
                }catch(err){
                    newCell.innerHTML =null
                }
            }
            if (["account_number"].includes(column)){
                let data = obj[column]
                if (data){newCell.innerHTML = data}
                
            }
            if (["name","status","op","method","gap_or_warr_cancelation_required","comments"].includes(column)){
                let data = obj[column]
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
            if(column === "customer_number"){
                newCell.innerHTML = '<a href="/pif/'+obj[column]+'">'+obj[column]+'</a>';
                newCell.style.textAlign = "left";
            }
            if (["date_pif","op_sent","date_canceled","ttl-cntrct_recd","ttl-cntrct_sent",].includes(column)){
                try{
                    let date = obj[column].toDate();
                    newCell.innerHTML = String(date.getMonth()+1)+'/'+String(date.getDate())+'/'+String(date.getFullYear());
                    newCell.setAttribute('data-sortable-type', 'date');
                    newCell.setAttribute('data-sortable-value', date);
                }catch(err){
                    newCell.innerHTML =null
                }
            }
            if (["account_number"].includes(column)){
                let data = obj[column]
                if (data){newCell.innerHTML = data}
                
            }
            if (["name","status","op","method","gap_or_warr_cancelation_required","comments"].includes(column)){
                let data = obj[column]
                newCell.innerHTML = data
            }
    
        });
    }
    const accountingView = {
        "customer_number":{"type":"numeric","display":"Customer Number"},
        "account_number":{"type":"numeric","display":"Account Number"},
        "name":{"type":"string","display":"Name"},
        "date_pif":{"type":"date","display":"PIF Date"},
        "status":{"type":"string","display":"Status"},
        "op":{"type":"string","display":"O/P"},
        "method":{"type":"string","display":"Method"},
        "op_sent":{"type":"string","display":"O/P Send"},
        "gap_or_warr_cancelation_required":{"type":"string","display":"gap_or_warr_cancelation_required"},
        "date_canceled":{"type":"date","display":"Date Canceled"},
        "ttl-cntrct_recd":{"type":"date","display":"ttl-cntrct_recd"},
        "ttl-cntrct_sent":{"type":"date","display":"ttl-cntrct_sent"},
        "comments":{"type":"string","display":"comments"},
    }
    
    function count_pif(snapshot){
        document.getElementById('alert-light').innerHTML = 'Count: ' + snapshot.size
    }
    function refresh_data() {
        tableRef.innerHTML = '';
        db.collection("pif_log").orderBy("date_pif","desc")
            .get()
            .then(function (querySnapshot) {
                querySnapshot.forEach(function (doc) {
                    createRow(doc.data(),Object.keys(accountingView));
                });
                count_pif(querySnapshot)
            })
            .catch(function (error) {
                console.log("Error getting documents: ", error);
            });
    
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
        loan_amount = document.getElementById('search_loan').value
        //location.reload("forceGet")
        console.log(loan_amount)
        display_loan_filter();
    }
    function display_loan_filter(){
        if (loan_amount!=""){
            var repo = document.getElementById("repo-log")
            repo.style.display='none';
            var repo_filer =document.getElementById('log_filter')
            repo_filer.getElementsByTagName("tbody")[0].innerHTML=""
            repo_filer.style.display='block'
    
            db.collection("pif_log").where("customer_number", "==" ,(loan_amount))
            .get()
            .then(function (querySnapshot) {
                    querySnapshot.forEach(function (doc) {
    
                        createRowNew(doc.data(), Object.keys(accountingView));
                    });
                    //updateHeaderDisplay(querySnapshot);
                    document.getElementById('search_loan').value="";
                    //document.getElementById('alert-light').innerHTML = 'count: ' + querySnapshot.size;
                })
                .catch(function (error) {
                    console.log("Error getting documents: ", error);
                });
        }else{
            var repo = document.getElementById("repo-log")
            repo.style.display='block';
            location.reload("forceGet")
            //refresh_data()
        }
    }