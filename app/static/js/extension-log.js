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