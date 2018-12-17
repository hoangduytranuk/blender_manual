## Đề án phiên dịch bản hướng dẫn sử dụng Blender (_Blender Reference Manual_)

# Chuẩn bị (_Preparations_)
- Tốt nhất là sử dụng hệ điều hành Linux, hoặc cài phần bằng cách cài đặt Hệ Thống Phụ Linux (**WSL**) trên "phiên bản Windows 10. Phương pháp  đã được ghi lại trên các trang này:

  . [Hướng dẫn cài đặt trên Windows 10 -- Windows 10 Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
  
  . [Thủ công tải về máy các gói phân phối của WSL (Linux) -- Manually download WSL distro packages](https://docs.microsoft.com/en-us/windows/wsl/install-manual)
  
  . [Khởi thủy bản phân phối vừa cài đặt xong -- Initializing a newly installed distro](https://docs.microsoft.com/en-us/windows/wsl/initialize-distro)

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

## Cập nhật hệ thống phụ Linux

Bản mà bạn đã tải xuống và cài đặt có thể không phải là phiên bản mới nhất, vì vậy hãy chạy các lệnh sau để cập nhật môi trường:

  `sudo apt-get update`
  
  `sudo apt-get upgrade`
  
  `sudo apt-get install -y git subversion`

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

## Đăng ký tài khoản và tham gia làm một người đóng góp và đề án

- Vào trang này: https://github.com/
- Bấm nút 'Sign up'
- Điền tên người dùng vào ô 'Username'. Nên dùng kiểu sau: hoangduytran1960 (không có dấu và không có khoảng trống cách chữ, cộng với năm sinh hoặc một số nào đấy)
- Điền thư điện tử vào ô 'Email address'
- Điền mật mã vào ô 'Password' (nhớ ghi lại vào đâu đó để về sau có quên thì lấy lại được) (Yêu cầu: 8 ký tự trở lên, gồm A-Z, 0-9, và có chữ Hoa, chữ Thường)
- Bấm Verify và xem xem nó bảo làm gì để nó biết là mình không phải là thông tin từ máy mà là người thật.
- Sau khi làm xong thì báo cho tôi biết tên người dùng vào e-mail của tôi (hoangduytran1960@gmail.com) để tôi thêm vào làm người đóng góp  (collaborator) và đặt quyền cho bạn được gửi các thay đổi lên đề án này.

## Lấy bản nguồn này xuống máy 

- Bằng dòng lệnh:

        git clone -b development https://github.com/hoangduytranuk/blender_manual.git

- Tất cả các bài có nội dung tiếng Việt cần sửa, dịch nằm ở trong thư mục:
        
        ~/blender_docs/locale/vi/LC_MESSAGES     

- ~/blender_docs là thư mục gốc
- Làm theo hướng dẫn ở trang này: (chọn hệ điều hành tương thích với cái mình đang sử dụng). Ví dụ dưới đây là trong hệ điều hành Linux Ubuntu/Mint :
        
        https://docs.blender.org/manual/vi/dev/about/contribute/install/index.html
        
  như lấy các phần mềm cần có xuống máy:
        
            sudo apt-get install python python-pip git subversion
            cd ~/blender_docs
            sudo pip install -r requirements.txt
            
  và trang này:
        
        https://docs.blender.org/manual/vi/dev/about/contribute/build/index.html
        
  như biên tập bản tiếng Việt:
            
        make -d --trace -w -B -e SPHINXOPTS="-D language='vi'" 2>&1                
            
- Bạn nên tạo 2 biến môi trường sau và ghi vào trong tập lệnh '.bashrc' để 

      export BLENDER_MAN_EN=$HOME/<thư mục tới>/blender_docs
      export BLENDER_MAN_VI=$BLENDER_MAN_EN/locale/vi

- Các tập tin mới được tạo sẽ chứa một số từ cần điền cho tác giả và ngày sửa đổi v.v. Nếu bạn cảm thấy công việc thay thế chúng lặp đi lặp lại, tẻ nhạt, thì hãy sử dụng tập lệnh 

      change_placeholders.sh 

trong thư mục con 

    ~/blender_docs/toos_maintenance

Sao lấy một bản vào thư mục **bin** địa phương của bạn và thay tất cả các giá trị đề cập trong tập tin với các chi tiết cụ thể của mình, rồi sau mỗi lần thay đổi một tập tin phiên dịch, bạn nên thực hiện các lệnh sau:

    $HOME/bin/change_placeholders.sh $BLENDER_MAN_VI
    
    make -d --trace -w -B -e SPHINXOPTS="-D language='vi'" 2>&1

Xem các thay đổi ở địa phương bằng cách dùng trình duyệt mạng, vào thư mục

    $BLENDER_MAN_EN/build/html/index.html

Nên lưu địa chỉ này vào mục ưa thích (Favorites) (Ctrl+D) của trình duyệt mạng để lần sau cứ vào đấy bấm vào để xem trang đầu, F5 (làm tươi lại - refresh) để lấy các thay đổi gần đây nhất mà không phải mở lại 

- Khi thay đổi xong và muốn nhập kho thì làm như sau:
    + xem các thay đổi:
    
          git status
          
    + nhập kho vào ổ địa phương:
        - (chỉ làm một lần, báo cho git biết là không ký lần nhập kho bằng mật mã riêng của cá nhân)
            
                git config commit.gpgsign false 

         - (cái này chỉ làm một lần, báo cho git là lưu trữ tên người dùng và mật mã, dùng cho những lần sau)

                git config credential.helper store 
        
         - (Đưa vào kho địa phương ở máy)
            
                git commit -am "<ghi chú về những gì đã làm trong thay đổi vừa rồi>"
        
         - (chuyển giao các thay đổi vào kho trên mạng, ở chi nhánh 'development')
        
                git push 

## Cài đặt bản *exclude* để bỏ qua những văn bản không cần thiết

- Để tạo bản html ở máy PC địa phương của mình, lệnh **make** sẽ kiến tạo một số các thư mục, văn bản dành riêng cho mình, song những văn bản, thư mục này không cần thiết phải lưu lại và chúng sẽ thay đổi thường xuyên nữa. Để báo cho **git** bỏ qua chúng thì chúng ta phải biên soạn bản:

      ~/.git/info/exclude

  dùng hoặc là *kate*, hoặc là *vi*, hoặc *nano*, và điền nội dung sau ở dưới cùng, sau các dòng khởi đầu bằng *#*:
  
      blender_docs/build
      *.mo
      *.pyc

  lưu các thay đổi, trước khi quay trở lại thư mục *blender_docs* và chạy lệnh:
  
      git status

  để xem danh sách các thay đổi.
  
## Các tập lệnh có thể cần sử dụng 

- Trong khi làm việc, việc tái thi hành lệnh đã làm trước đây sẽ là một việc không tránh khỏi, chẳng hạn như lệnh tạo *html*. Tốt nhất là kèm chúng vào một tập lệnh ở thư mục **bin** địa phương và đặt nó là có quyền thi hành:
    1. Lệnh **makevidoc.py** trong dạng tập lệnh *Python*:


```Python
#!/usr/bin/python3 -d
import os
from argparse import ArgumentParser

class MakingVIDocuments:
    def __init__(self):
        self.is_clean : bool = False
        self.make_dir : str = None

    def setVars(self, is_clean : bool, make_dir: str):
        self.is_clean = (True if (is_clean) else False)
        self.make_dir = (os.environ['BLENDER_MAN_EN'] if (make_dir == None) else make_dir)
        
    def run(self):
        os.chdir(self.make_dir)
        if (self.is_clean):
            os.system("make clean")
            os.system("find locale/vi/LC_MESSAGES -type f -name \"*.mo\" -exec rm -f {} {} \;")
            
        os.system("make -d --trace -w -B -e SPHINXOPTS=\"-D language='vi'\" 2>&1")
        
parser = ArgumentParser()
parser.add_argument("-c", "--clean", dest="clean_action", help="Xóa sạch các thư mục trước khi thi hành MAKE.", action='store_true')
parser.add_argument("-d", "--dir", dest="make_dir", help="Thư mục nơi mà MAKE sẽ làm việc")
args = parser.parse_args()

print("args: {}".format(args))

x = MakingVIDocuments()
x.setVars(args.clean_action, args.make_dir)
x.run()
```
  + Lưu tập lệnh **makevidoc.py** này vào thư mục **$HOME/bin** của máy. Nhớ biên soạn bản *·bashrc* và đặt dòng sau để thư mục *$HOME/bin* nằm trong danh sách các đường dẫn mà hệ điều hành sẽ lùng tìm các bản tập lệnh khi chạy dòng lệnh:
  
      ```bash
        export MYBIN=$HOME/bin
        export PATH=$MYBIN:$PATH
      ```
      
  + Đặt tập lệnh này là **KHẢ THI HÀNH** bằng lệnh:
      ```bash
        chmod u+x $HOME/bin/makevidoc.py
      ```
  + Sau đó, chúng ta có thể chạy nó như các ví dụ sau:
      - Xem hướng dẫn sử dụng
      ```bash
        makevidoc.py --help
      ```
      - Thi hành **make** nhưng không xóa bản cũ đi, viết đè lên. Phương pháp này sẽ nhanh hơn, song nhiều khi sẽ không cho kết quả chính xác:
      ```bash
        makevidoc.py
      ```
      - Thi hành **make** và xóa bản cũ đi:
      ```bash
        makevidoc.py -c
      ```
      - Thi hành **make** và xóa bản cũ đi, định thư mục nơi nó cần làm việc là thư mục hiện tại ($PWD = Print Working Directory: In ra thư mục làm việc):
      ```bash
        makevidoc.py -c $PWD
      ```
      
      2. Lệnh **updatePO.sh**
        - Tập lệnh này cho phép mình điền tên và e-mail của mình vào phần *COMMENT* của các văn bản mà mình sửa, đồng thời điền ngày giờ mình đã làm nữa. Nó dùng lệnh **svn** và **git** để tìm các văn bản có đuôi là **.po** đã thay đổi. Nếu phải tự lùng tìm ở một thư mục nào đó không phải là thư mục có thư mục **.svn** hoặc **.git** thì nó sẽ tìm các văn bản có đuôi là **.po** mà thôi và cách này là cách làm việc lâu nhất.
        - Các từ mình cần điền chi tiết của cá nhân là:
        ```bash
          YOUR_NAME="Họ tên đầy đủ"
          YOUR_EMAIL="địa-chỉ-email@máy_chủ.com"
        ```
        
        
      
      
  
      
          
      
