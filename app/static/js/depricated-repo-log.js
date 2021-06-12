const tableRef = document.getElementById("repo-log").getElementsByTagName('tbody')[0];
        let status_array = ["Repo"];

        function removeItemAll(arr, value) {
            let i = 0;
            while (i < arr.length) {
                if(arr[i] === value) {
                    arr.splice(i, 1);
                } else {
                    ++i;
                }
            }
            return arr;
        }

        function update_filters(elem, list) {
            if (list.includes(elem)) {
                removeItemAll(list, elem);
                document.getElementById(elem).classList.remove('active');
                refresh_data();
            } else {
                list.push(elem);
                document.getElementById(elem).classList.add('active');
                refresh_data()
            }
            //console.log(list);
        }
        const standardView = ['loan', 'status', 'gaap_date', 'noi_sent', 'dafs', 'date_sold', 'co_date',
            'months_in_inventory', 'location', 'sold_to', 'cr_grade', 'chargeable_damages', 'balance_repo_date', 'awv', 'mmr',
            'cash_price', 'estimated_recovery', 'current_mo_proceeds_estimate', 'eom_gaap_proceeds_estimate',
            'actual_proceeds', 'back_end_product_cancellation', 'insurance_claims',
            'gross_co_amt', 'unearned_discount', 'net_loss_or_gain', 'recovery', 'rem_bal', 'cash_or_new_ac'];

        function financial(value) {
            let absValue = Math.abs(value);
            let returnString = Number(absValue).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2
            });
            return value < 0 ? '(' + returnString + ')' : returnString;
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
                        newCell.innerHTML = obj[column].toFixed(2);
                        newCell.setAttribute('data-value', obj[column].toFixed(2));
                        // display as number not money.
                    } else if (['estimated_recovery', 'acct_diff', 'pforma_diff', 'repo_allow2_hist'].includes(column)) {
                        // display as percentages
                        newCell.innerHTML = String((obj[column]*100).toFixed(1))+'%';
                        newCell.setAttribute('data-value', obj[column] * 100);
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

        let timePeriod = new Date(new Date(2018, 0, 1).toLocaleString('en-US', {'timeZone':'America/Chicago'}));
        let until = new Date(new Date().toLocaleString('en-US', {'timeZone':'America/Chicago'}))
        //console.log('starting timePeriod: ' + String(timePeriod));

        function lookBack(id_string) {
            let t = new Date(new Date().toLocaleString('en-US', {'timeZone':'America/Chicago'}));
            //console.log('t: ' + String(t));
            if (id_string === 'all') {
                timePeriod = new Date(2018, 0, 1);

            } else if (id_string === 'current-mo') {
                timePeriod = new Date(t.getFullYear(), t.getMonth(), 1);
                until = t;

            } else if (id_string === 'last-mo') {
                timePeriod = new Date(t.getFullYear(), t.getMonth() - 1, 1);
                until = new Date(t.getFullYear(), t.getMonth(), 1, -1, 59, 59);
            } else if (id_string === 'last-90') {
                timePeriod = new Date(new Date().setDate(new Date().getDate() - 90));
                until = t;
            } else if (!id_string){
                timePeriod = new Date(new Date(2018, 0, 1).toLocaleString('en-US', {'timeZone':'America/Chicago'}));
            }

            document.getElementById('last-90').classList.remove('active');
            document.getElementById('current-mo').classList.remove('active');
            document.getElementById('last-mo').classList.remove('active');
            document.getElementById('all').classList.remove('active');
            document.getElementById(id_string).classList.add('active');
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
            //console.log(day, month, year);
            return(`${month}/${day}/${year }`);
        }


        function refresh_data() {
            tableRef.innerHTML = '';
            //console.log('START: ' + String(timePeriod));
            //console.log('STOP: ' + String(until));
            document.getElementById('date-range').innerText = 'Repo GAAP date range: ' + displayDate(timePeriod) + ' - ' + displayDate(until);
            document.getElementById('date-range').style.marginLeft = '15px';
            document.getElementById('date-range').style.fontWeight = 'bold';

            db.collection("repos")
                .where("status", "in", status_array)
                .where("gaap_date", "<=", until) // stop date (most recent)
                .where("gaap_date", ">=", timePeriod) // start date
                .orderBy("gaap_date", "desc")
                .get()
                .then(function (querySnapshot) {
                    querySnapshot.forEach(function (doc) {
                        createRow(doc.data(), standardView);
                    });
                })
                .catch(function (error) {
                    console.log("Error getting documents: ", error);
                });
        }
        window.onload = function() {
            refresh_data();
        }