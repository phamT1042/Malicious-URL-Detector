document.addEventListener("DOMContentLoaded", function () {
  // Truy vấn thông tin về tab đang được chọn trong cửa sổ hiện tại
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {

    // Lấy URL của tab đang được chọn và đặt giá trị vào thẻ input có id là "url-input"
    var url = tabs[0].url;
    document.getElementById("url-input").value = url;

    // Gọi hàm checkMalicious với URL và một chuỗi "check" làm đối số
    checkMalicious(url, "check");
  });

  // Khi người dùng submit form
  document
    .getElementById("url-form")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      // Lấy giá trị của URL từ thẻ input có id là "url-input1"
      var url = document.getElementById("url-input1").value;
      checkMalicious(url, "result");
    });
});

// Hàm kiểm tra tính an toàn của URL
function checkMalicious(url, classname) {
  // Gửi yêu cầu GET đến một API máy học với URL như là một tham số truy vấn
  fetch(`http://127.0.0.1:8000/api?url=${url}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    // Xử lý phản hồi từ API
    .then((response) => response.json())
    .then((data) => {
      // Lấy giá trị đầu tiên từ mảng JSON được trả về
      let test = data[0];

      // Lấy phần tử HTML có class là classname
      var resultDiv = document.getElementsByClassName(classname)[0];
      // Nếu giá trị là một chuỗi, hiển thị nó trong phần tử
      if (Array.isArray(test)) {
        if (test[0]) {
          resultDiv.innerHTML = `Đường dẫn này có tỉ lệ ${(test[1] * 100).toFixed(2)}% dẫn đến trang web độc hại`;
          resultDiv.style.color = "red";
        }
        else {
          resultDiv.innerHTML = `Đường dẫn này có tỉ lệ ${(test[1] * 100).toFixed(2)}% dẫn đến trang web an toàn`;
          resultDiv.style.color = "green";
        }
      } else {
        // Nếu không, hiển thị thông báo từ trường "msg" trong dữ liệu
        resultDiv.innerHTML = data.msg;
      }

    })
    .catch((error) => {
      alert("Error:", error);
    });
}
