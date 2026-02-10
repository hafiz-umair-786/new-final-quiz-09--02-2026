document.getElementById("signupBtn").addEventListener("click", async () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/api/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (data.success) {
    alert("Signup successful!");
    window.location.href = "/quiz"; // redirect to quiz
  } else {
    alert("Signup failed: " + data.error);
  }
});
