// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAyuspBd2bLb0HACemyC4rSKk94nCINmhU",
  authDomain: "python30-d2360.firebaseapp.com",
  projectId: "python30-d2360",
  storageBucket: "python30-d2360.firebasestorage.app",
  messagingSenderId: "1009829516500",
  appId: "1:1009829516500:web:c250d18d6a5f27a1b65741"
};

// Initialize Firebase
//const app = initializeApp(firebaseConfig);
// Inicializa
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);