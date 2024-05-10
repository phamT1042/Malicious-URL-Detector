document.addEventListener("DOMContentLoaded", function () {
    // Truy vấn thông tin về tab đang được chọn trong cửa sổ hiện tại
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      
      // Lấy URL của tab đang được chọn và đặt giá trị vào thẻ input có id là "url-input"
      var url = tabs[0].url;
      document.getElementById("url-input").value = url;
  
      // Gọi hàm checkPhishing với URL và một chuỗi "check" làm đối số
      checkPhishing(url, "check");
    });
  
    // Khi người dùng submit form
    document
      .getElementById("url-form")
      .addEventListener("submit", function (event) {
        event.preventDefault();
        // Lấy giá trị của URL từ thẻ input có id là "url-input1"
        var url = document.getElementById("url-input1").value;
        checkPhishing(url, "result");
      });
  });
  
  // Hàm kiểm tra tính an toàn của URL
  function checkPhishing(url, classname) {
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
        // Hiển thị giá trị đầu tiên trong console và kiểu dữ liệu của nó
  
        // Lấy phần tử HTML có class là classname
        var resultDiv = document.getElementsByClassName(classname)[0];
        // Nếu giá trị là một chuỗi, hiển thị nó trong phần tử
        if (typeof test === "string") {
          resultDiv.innerHTML = test;
        } else {
          // Nếu không, hiển thị thông báo từ trường "msg" trong dữ liệu
          resultDiv.innerHTML = data.msg;
        }
  
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  