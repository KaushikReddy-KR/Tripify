const firebaseConfig = {
    apiKey: "AIzaSyCOYnZXCnnBOzWyFXIDcxyU3d-GxNXFqZA",
    authDomain: "shuttle-service-a18db.firebaseapp.com",
    databaseURL: "https://shuttle-service-a18db-default-rtdb.firebaseio.com",
    projectId: "shuttle-service-a18db",
    storageBucket: "shuttle-service-a18db.appspot.com",
    messagingSenderId: "1048175234280",
    appId: "1:1048175234280:web:117002bbc27dd98ab84d5d"
  };

  firebase.initializeApp(firebaseConfig);
  
var database = firebase.database()
//console.log('alo')
function save(){
    var name=document.getElementById("inputName").value
    var rollno=document.getElementById("inputRoll").value
    var email_id=document.getElementById("inputEmail1").value
    var pass=document.getElementById("inputPassword1").value
    //console.log("hello")
    database.ref('shuttleService/'+ rollno).set({
        name : name,
        rollno : rollno,
        email_id : email_id,
        pass : pass
    })
    alert('Saved')
}