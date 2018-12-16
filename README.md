## Đề án phiên dịch bản hướng dẫn sử dụng Blender (_Blender Reference Manual_)

# Chuẩn bị (_Preparations_)
- Tốt nhất là sử dụng hệ điều hành Linux, hoặc cài phần bằng cách cài đặt Hệ Thống Phụ Linux (**WSL**) trên "phiên bản Windows 10. Phương pháp  đã được ghi lại trên các trang này:

  . [Hướng dẫn cài đặt trên Windows 10 -- Windows 10 Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
  . [Thủ công tải về máy các gói phân phối của WSL (Linux) -- Manually download WSL distro packages](https://docs.microsoft.com/en-us/windows/wsl/install-manual)
  . [Khởi thủy bản phân phối vừa cài đặt xong -- Initializing a newly installed distro](https://docs.microsoft.com/en-"
"us/windows/wsl/initialize-distro)

Điều này sẽ cho phép bạn truy cập vào tính năng phong phú mà môi trường dòng lệnh Linux cung cấp.

## Kiểm tra phiên bản Linux hiện có

Trước tiên, hãy kiểm tra phiên bản Linux có sẵn tại trang web phân phối. Trong ví dụ này, chúng tôi đã chọn Ubuntu Desktop 18.04. Bạn có thể tìm hiểu thêm về phiên bản mới nhất [tại đây](https://www.ubuntu.com/download/desktop)

## Cài đặt hệ thống phụ Linux

Có thể cách tốt hơn là cài đặt bằng cách sử dụng *PowerShell*. Mở *PowerShell* bằng cách nhập tên vào hộp tìm kiếm *Cortana*. Nhấp chuột phải vào mục *PowerShell* tìm thấy và chọn thi hành với tư cách *Quản trị viên* (run as Administrator). Điều đầu tiên, chúng ta cần kích hoạt hệ thống phụ Linux, sử dụng dòng lệnh sau:

  `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux`

Khi làm xong, tắt nguồn và khởi động lại hệ thống là điều bắt buộc, vì vậy, hãy khởi động lại hệ thống. Khi hệ thống được bật trở lại, hãy quay lại *PowerShell* và nhập lệnh sau:

  `Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu.appx -UseBasicParsing`

Việc làm này sẽ tải xuống Linux Ubuntu và lưu trữ trong tập tin Ubuntu.appx tại thư mục làm việc hiện tại, như được chỉ rõ trong tham số **-OutFile**. Bạn có thể chọn di chuyển nó sang thư mục khác sau khi tải xuống hoàn tất, bằng cách thực hiện:

  `mv Ubuntu.appx 'c:\Users\<your username>\Downloads'`

Khi tập tin Ubuntu.appx đã được lấy xuống, sử dụng Explorer và xem thư mục lấy xuống, đảm bảo rằng tập tin nằm ở đó, sau đó nhấp đúp vào Ubuntu.appx để chạy cài đặt, nhập tên người dùng, và Mật Khẩu, cộng với xác minh mật khẩu cho tài khoản người dùng như được hiển thị trong cửa sổ dòng lệnh.

Khi quá trình cài đặt hoàn tất, bạn có thể tìm thấy biểu tượng của Ubuntu trong Start Menu (Nút trình đơn Bắt Đầu), hoặc tìm kiếm trong Cortana, bằng cách gõ Ubuntuvào hộp tìm kiếm. Sau đó bạn có thể thực hiện một hoặc cả hai trong số những điều sau đây:


    Bấm chuột phải và chọn Ubuntu 18.04 ‣ Đính vào trình đơn bắt đầu (pin to start)
    Bấm chuột phải và chọn Ubuntu 18.04 ‣ thêm (more) ‣ Đính vào thanh tác vụ (pin to taskbar)

## Cập nhận hệ thống phụ Linux

Bản mà bạn đã tải xuống và cài đặt có thể không phải là phiên bản mới nhất, vì vậy hãy chạy các lệnh sau để cập nhật môi trường:

  `
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get install -y subversion
  `
Bạn còn có thể tải xuống máy bản [Kate trên Windows](https://kate-editor.org/2016/01/28/kate-on-windows/) làm một trình biên soạn văn bản bổ sung, thay cho cái hiện tại đang sử dụng.

## Lưu Ý

Vị trí của bản Ubuntu 18.04 nằm tại:

    C:\Users\<windows username>\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs\home\<Ubuntu's username>

Mình có thể tìm thấy ánh xạ của ổ đĩa C: bằng cách sử dụng:
  mount
    và nó thường nằm ở:

    C: on /mnt/c type drvfs (rw,noatime)

Lệnh

    xdg-open /home/<username>/blender_docs/build/html/index.html

  không hoạt động. Bạn sẽ phải chỉnh sửa .bashrc bằng cách sử dụng nano hoặc vi, chọn cái nào mà cảm thấy mình quen thuộc nhất - nano có lẽ là lựa chọn tốt hơn khi bạn không thực sự cần phải học nhiều và danh sách phím tắt ở phía dưới sẽ giúp bạn bắt đầu nhanh hơn - và tạo một biến môi trường ở cuối tập tin, giống như sau:

    export WIN_HOME=/mnt/c/Users/<windows_account_name>

Địa điểm này giống hệt %userprofile%. Nạp lại .bashrc tại dấu nhắc lệnh:

    . ./.bashrc

sau đó thay đổi thư mục làm việc hiện tại thành WIN_HOME:

    cd "$WIN_HOME"

Trước khi bắt đầu phần tiếp theo để xuất kho mã nguồn viết tài liệu.

Một khi make html đã được thực hiện, bạn có thể sử dụng trình duyệt mạng của bạn để tiếp cận thư mục blender_docs tại **%userprofile%**  của bạn và xem tập tin 

  `index.html` 

tại thư mục **blender_docs**. Sau khi xem, bạn có thể đánh dấu địa chỉ trang trên *Dấu trang ưa thích* (Favorite Bookmarks) của trình duyệt mạng, cho phép bạn truy cập trang này nhanh hơn ở những lần sau.

Sau khi làm xong hướng dẫn ở trên thì bạn đã sẵn sàng làm theo quy trình cài đặt như đề cập đến trong 




- Vào trang này: https://github.com/ và bấm vào nút **Sign up** để đăng ký cho bản thân mình 

You can use the [editor on GitHub](https://github.com/hoangduytranuk/blender_manual/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/hoangduytranuk/blender_manual/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
