# Đề án phiên dịch bản hướng dẫn sử dụng Blender (_Blender Reference Manual_)

## Lấy bản ZIP mới nhất của bản hướng dẫn sử dụng hiện đang làm:

Có hai bản hiện được biên tập:

- Tất cả nội dung nằm trong [một tập tin index.html](blender_docs/build/blender_vietnamese_single.zip)
- Nội dung được phân ra [nhiều bản html, mỗi tập tin một đề mục riêng](blender_docs/build/blender_vietnamese_html.zip)

## Lấy bản phiên dịch giao diện *blender.mo* cho:
- Phiên bản [2.79](gui/2.79/locale/vi/LC_MESSAGES/blender.mo)
- Phiên bản [2.80](gui/2.80/locale/vi/LC_MESSAGES/blender.mo)
Lưu ý: Xin xem hướng dẫn ở địa chỉ cũ [này](https://github.com/hoangduytran/blender-internationalisation/blob/master/README.md) để xem cách cài đặt bản *blender.mo* vào thư mục của phần mềm Blender.

## Chuẩn bị (Preparations)

Tốt nhất là [cài đặt và sử dụng hệ điều hành Linux](https://www.youtube.com/watch?v=uzpKjeZykoQ&list=PL9LmhZmBx5yBIcEMwhVcLn7mtlGWW2HWu). Nếu không làm được thì học cài đặt Hệ Thống Phụ Linux (**WSL**) trên phiên bản Windows 10. Phương pháp  đã được ghi lại trên các trang này:

+ [Hướng dẫn cài đặt trên Windows 10 -- Windows 10 Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

+ [Thủ công tải về máy các gói phân phối của WSL (Linux) -- Manually download WSL distro packages](https://docs.microsoft.com/en-us/windows/wsl/install-manual)

+ [Khởi thủy bản phân phối vừa cài đặt xong -- Initializing a newly installed distro](https://docs.microsoft.com/en-us/windows/wsl/initialize-distro)

Điều này sẽ cho phép bạn truy cập vào tính năng phong phú mà môi trường dòng lệnh Linux cung cấp.


## Kiểm tra phiên bản Linux hiện có (Find the current release's version)

Trước tiên, hãy kiểm tra phiên bản Linux có sẵn tại trang web phân phối. Trong ví dụ này, chúng tôi đã chọn **Ubuntu Desktop 18.04**. Bạn có thể tìm hiểu thêm về phiên bản mới nhất [tại đây](https://www.ubuntu.com/download/desktop)

## Cài đặt hệ thống phụ Linux (Setup the Linux subsystem)

Có thể cách tốt hơn là cài đặt bằng cách sử dụng *PowerShell*. Mở *PowerShell* bằng cách nhập tên vào hộp tìm kiếm *Cortana*. Nhấp chuột phải vào mục *PowerShell* tìm thấy và chọn thi hành với tư cách *Quản trị viên* (run as Administrator). Điều đầu tiên, chúng ta cần kích hoạt hệ thống phụ Linux, sử dụng dòng lệnh sau:

        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

Khi làm xong, tắt nguồn và khởi động lại hệ thống là điều bắt buộc, vì vậy, hãy khởi động lại hệ thống. Khi hệ thống được bật trở lại, hãy quay lại *PowerShell* và nhập lệnh sau:

        Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu.appx -UseBasicParsing

Việc làm này sẽ tải xuống *Linux Ubuntu* và lưu trữ trong tập tin `Ubuntu.appx` tại thư mục làm việc hiện tại, như được chỉ rõ trong tham số `-OutFile`. Bạn có thể chọn di chuyển nó sang thư mục khác sau khi tải xuống hoàn tất, bằng cách thực hiện:

```bash
  mv Ubuntu.appx 'c:\Users\<your username>\Downloads'
```

Khi tập tin `Ubuntu.appx` đã được lấy xuống, sử dụng *Explorer* và xem thư mục lấy xuống, đảm bảo rằng tập tin nằm ở đó, sau đó nhấp đúp vào `Ubuntu.appx` để chạy cài đặt, nhập tên người dùng, và mật khẩu, cộng với xác minh mật khẩu cho tài khoản người dùng như được hiển thị trong cửa sổ dòng lệnh.

Khi quá trình cài đặt hoàn tất, bạn có thể tìm thấy biểu tượng của *Ubuntu* trong *Start Menu* (nút trình đơn *Bắt Đầu*), hoặc tìm kiếm trong *Cortana*, bằng cách gõ `Ubuntu` vào hộp tìm kiếm. Sau đó bạn có thể thực hiện một hoặc cả hai trong số những điều sau đây:

    Bấm chuột phải và chọn Ubuntu 18.04 ‣ Đính vào trình đơn bắt đầu (pin to start)
    Bấm chuột phải và chọn Ubuntu 18.04 ‣ thêm (more) ‣ Đính vào thanh tác vụ (pin to taskbar)

## Cập nhật hệ thống phụ Linux (Updating the Linux subsystem)

+ Bản mà bạn đã tải xuống và cài đặt có thể không phải là phiên bản mới nhất, vì vậy hãy chạy các lệnh sau để cập nhật môi trường:

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y git subversion

+ Bạn còn có thể tải xuống máy bản [Kate trên Windows](https://kate-editor.org/2016/01/28/kate-on-windows/) làm một trình biên soạn văn bản bổ sung, thay cho cái hiện tại đang sử dụng. Cái này cho phép nêu bật các chữ chìa khóa của tập tin **.po** phiên dịch, dễ làm việc hơn trên giao diện đồ họa.


## Lưu Ý (Note)

+ Vị trí của bản Ubuntu 18.04 nằm tại:

        C:\Users\<windows username>\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs\home\<Ubuntu's username>

    Mình có thể tìm thấy ánh xạ của ổ đĩa C: bằng cách sử dụng:

        mount

    và nó thường nằm ở:

        C: on /mnt/c type drvfs (rw,noatime)

+ Lệnh

        xdg-open /home/<username>/blender_docs/build/html/index.html

    không hoạt động. Bạn sẽ phải chỉnh sửa **.bashrc** bằng cách sử dụng trình soạn văn bản ở chế độ dòng lệnh, tên là *nano* hoặc *vi*, chọn cái nào mà cảm thấy mình quen thuộc nhất - *nano* có lẽ là lựa chọn tốt hơn khi bạn không thực sự cần phải học nhiều và danh sách phím tắt ở phía dưới sẽ giúp bạn bắt đầu nhanh hơn - và tạo một biến môi trường ở cuối tập tin, giống như sau:

        export WIN_HOME=/mnt/c/Users/<windows_account_name>

    bản **.bashrc** trong Linux, Unix, macOS cũng tương tự như chức năng của bản *autoexec.bat* trong các phiên bản **Windows** cũ, nó khởi động khi mình bật cửa sổ dòng lệnh lên, nên tất cả các biến môi trường và dòng lệnh trong đó sẽ được thi hành trước, trước khi chúng ta sử dụng dòng lệnh.

    Địa điểm này giống hệt %userprofile%. Nạp lại **.bashrc** tại dấu nhắc lệnh:

        . ./.bashrc

    sau đó thay đổi thư mục làm việc hiện tại sang **$WIN_HOME** :

        cd "$WIN_HOME"

    trước khi bắt đầu phần tiếp theo để xuất kho mã nguồn viết tài liệu.

    Một khi `make html` đã được thực hiện, bạn có thể sử dụng trình duyệt mạng của bạn để tiếp cận thư mục blender_docs tại **\%userprofile\%**  của bạn và xem tập tin `index.html` tại thư mục **blender_docs**. Sau khi xem, bạn có thể đánh dấu địa chỉ trang trên *Dấu trang ưa thích* (Favorite Bookmarks) của trình duyệt mạng, cho phép bạn truy cập trang này nhanh hơn ở những lần sau.

------------------

## Đăng ký tài khoản và tham gia làm một người đóng góp vào đề án (Registering an user account and join to become a Project's collaborator)

- Vào trang [này](https://github.com/):

- Bấm nút **Sign up**

- Điền tên người dùng vào ô **Username**. Nên dùng kiểu sau: hoangduytran1960 (không có dấu và không có khoảng trống cách chữ, cộng với năm sinh hoặc một số nào đấy)

- Điền thư điện tử vào ô **Email address**

- Điền mật mã vào ô 'Password' (nhớ ghi lại vào đâu đó để về sau có quên thì lấy lại được) (Yêu cầu: 8 ký tự trở lên, gồm A-Z, 0-9, và có chữ Hoa, chữ Thường)

- Bấm **Verify** và xem xem nó bảo làm gì để nó biết là mình không phải là thông tin từ máy mà là người thật.

- Sau khi làm xong thì báo cho tôi biết tên người dùng vào e-mail của tôi [hoangduytran1960@gmail.com](mailto:hoangduytran1960@gmail.com) để tôi thêm vào làm người hợp tác  (collaborator) và đặt quyền cho bạn được gửi các thay đổi lên đề án này.

## Cài đặt các phần mềm cần thiết (Install required softwares)

Làm theo hướng dẫn ở trang [Cài Đặt -- Install](https://docs.blender.org/manual/vi/dev/about/contribute/install/index.html) chọn hệ điều hành tương thích với cái mình đang sử dụng). Ví dụ lấy các phần mềm cần có xuống máy dưới đây là trong hệ điều hành Linux Ubuntu/Mint:

        sudo apt-get install python python-pip git subversion


## Lấy bản nguồn này xuống máy (Downloading the project's source code and documents)

+ Bằng dòng lệnh:

        cd $HOME
        git clone https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git

+ Nếu cài Hệ Thống Phụ Linux (**WSL**) thì dùng:

        cd $WIN_HOME
        git clone https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git

+ Các thư mục sẽ tạo trong ổ cứng là

        blender_manual/
        ├── blender_docs

+ Trong thư mục `blender_manual` mình sẽ tìm thấy thư mục `.git`. Thư mục này là thư mục `git` sử dụng để lưu các thay đổi của mình, cùng có các thư mục khác như `info/exlude` mà mình sẽ nói đến sau này.

+ Tất cả các bài có nội dung tiếng Việt cần sửa, dịch nằm ở trong thư mục:

        $HOME/blender_manual/blender_docs/locale/vi/LC_MESSAGES

+ Thư mục `blender_manual/blender_docs` là thư mục gốc. Nhớ thay thế `\$HOME` sang `\$WIN_HOME` nếu dùng **WSL**.


## Cài đặt các phần mềm cần thiết cho việc biên tập (Install softwares necessary for compilation)

+ Lấy các phần mềm cần có để biên dịch xuống máy:

        sudo install build-essential git subversion
        cd $HOME/blender_manual/blender_docs
        sudo pip install -r requirements.txt

+ Nếu các bạn gặp khó khăn trong vấn đề về UTF-8 (tiếng Việt) trong khi biên soạn thì đổi sang sử dụng Python3, dùng lệnh:

        which python

    và lệnh:

        which python3

    để tìm xem địa chỉ của 'python' nằm ở đâu. Thường là ở '/usr/bin/'.

+ Lần vào đó và liệt kê để xem tên cụ thể:

        cd /usr/bin
        ls -alF python

    Thường thì mình sẽ thấy là 'python' là kết nối mềm (softlink) của 'python2.7', và 'python3' là kết nối mềm của 'python3.6'

+ Đổi lệnh từ 'python' sang dùng 'python3', để khi đánh 'python' thì hệ điều hành tự động sử dụng 'python3':

        sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
        sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

    Nếu đánh dòng lệnh:

        sudo update-alternatives --config python

    thì mình sẽ thấy bảng liệt kê của các lệnh trong bảng 'alternatives' (những phương án thay thế có thể sử dụng), ví dụ:

        There are 2 choices for the alternative python (providing /usr/bin/python).
        (Có 2 lựa chọn về phương án thay thế Python (chu cấp cho /usr/bin/python).)

| Selection (Lựa Chọn) | Path (Đường Dẫn) | Priority (Ưu Tiên) | Status (Trạng Thái) | Comment (Ghi Chú) |
| --- | --- | :---: | --- | --- |
| *0 | /usr/bin/python3.6 | 2 | auto mode | (chế độ tự động) |
| 1 | /usr/bin/python2.7 | 1 | manual mode | (chế độ thủ công) |
| 2 | /usr/bin/python3.6 | 2 | manual mode | (chế độ thủ công) |

        Press <enter> to keep the current choice[*], or type selection number:
        (Bấm phím <enter> để duy trì lựa chọn hiện tại [*], hoặc điền số mình lựa chọn:)

+ Để đổi lại sử dụng python2.7 thì điền 1, rồi bấm phím Enter, để khi đánh 'python' thì nó sử dụng bản '2.7'. Để đổi lại sử dụng python3.6 thì điền 2, để khi đánh 'python' thì nó sử dụng bản '3.6'. Đánh lệnh:

        man update-alternatives

    để xem bảng hướng dẫn sử dụng.

+ Cài đặt như hướng dẫn nhưng dùng 'pip3':

        sudo apt-get -y install python3-pip
        cd $HOME/blender_manual/blender_docs
        sudo pip3 install -r requirements.txt

+ Biên tập bản tiếng Việt dùng lệnh:

        make -d --trace -w -B -e SPHINXOPTS="-D language='vi'" 2>&1

+ Cài đặt git:

        cd $HOME/blender_manual/blender_docs


+ Đặt tên người dùng:

        git config --global user.name "Tên đầy đủ"

+ Đăt địa chỉ e-mail:

        git config --global user.email "địa-chỉ@máy-chủ.com"

+ Những thông tin này thường được ghi ở tập tin `.gitconfig` ở thư mục **\$HOME**

        [user]
            name = Hoang Duy Tran
            email = hoangduytran1960@googlemail.com
            signingkey = ?????????
        [core]
            editor = gedit -s
        [commit]
            gpgsign = false
        [gpg]
            program = gpg2
        [gui]
            recentrepo = <đường dẫn đến thư mục git>

    Xem ví dụ ở đây [brettz9/.gitconfig](https://gist.github.com/brettz9/8d8b6315f7d8f90edec0)

------------------

## Biến môi trường cần thiết (Important environment variables)

Bạn nên tạo 2 biến môi trường sau và ghi vào trong tập lệnh **.bashrc** để đơn giản hóa việc sử dụng dòng lệnh, tránh việc nhắc đi, nhắc lại. Tập lệnh này nằm ở địa chỉ **\$HOME** của mình:

        export BLENDER_MAN_EN=$HOME/blender_manual/blender_docs
        export BLENDER_MAN_VI=$BLENDER_MAN_EN/locale/vi


<!--  -->
## Cài đặt bản *exclude* để bỏ qua những văn bản không cần thiết (Configuring the *exclude* file to ignore objects)

Để tạo bản html ở máy PC địa phương của mình, lệnh **make** sẽ kiến tạo một số các thư mục, văn bản dành riêng cho mình, song những văn bản, thư mục này không cần thiết phải lưu lại và chúng sẽ thay đổi thường xuyên nữa. Để báo cho **git** bỏ qua chúng thì chúng ta phải biên soạn bản:

        .git/info/exclude

dùng hoặc là **kate**, hoặc là **vi**, hoặc **nano**, và điền nội dung sau ở dưới cùng, sau các dòng khởi đầu bằng *#*:

        blender_docs/build
        *.mo
        *.pyc

lưu các thay đổi, trước khi quay trở lại thư mục **blender_docs** và chạy lệnh:

        git status

để xem danh sách các thay đổi.


------------------

## Quy trình làm việc đề cử, tuy không bắt buộc (Proposed operating procedure)

+ Học thêm về cách sử dụng **git**. Tìm trên mạng dùng từ *hướng dẫn sử dụng git*.
+ Tạo một chi nhánh cho mình để thử nghiệm và nếu cần thì có thể xóa chi nhánh đó đi.

        cd $BLENDER_MAN_EN
        git checkout -b <tên chi nhánh>

+ Sau các sửa đổi thì dùng lệnh sau để chuyển vào kho địa phương của mình:

        git commit -am "Lời miêu tả những thay đổi"

+ Muốn bỏ các thay đổi ở `git_dia_phuong` thì có thể dùng:

        git status

+ Để xem các thay đổi và đường dẫn của các tập tin đã thay đổi.

        git stash

+ Để cất giấu các thay đổi để sau này mình có thể lấy lại nếu muốn.

        git checkout -- <filename>

+ Để bỏ các thay đổi trong tập tin <filename> hoàn toàn, lấy lại nội dung cũ.

        git reset --hard

+ Để bỏ tất cả các thay đổi, không bao giờ lấy lại được nữa. Cẩn thận với lệnh này.

+ Quay trở lại một phiên bản nào đó:

        git log --all --decorate --oneline --graph

    cho mình xem danh sách các thay đổi và thấy số mã của các lần commit, đồng thời cho thấy mũi tên hiện nay đang chỉ vào chi nhánh nào, vào `master` hay một chi nhánh nào đó. Ghi nhớ hoặc dùng chuột quét và chọn số mã đó. Mìn còn có thể bấm chuột phải và chọn 'Copy' để đưa vào bộ nhớ. (Xem cách tạo lệnh viết tắt ở cuối bài để khỏi phải đánh lại các lệnh dài, hay sử dụng, nhiều lần)

        git checkout <số mã phiên bản commit>

    bấm bánh xe chuột xuống để lấy con số mà mình đã chọn ở trên. Nếu đã chọn và 'Copy' vào bộ nhớ dùng bấm chuột phải thì có thể sử dụng bấm chuột phải và chọn 'Paste' để dán số mã từ bộ nhớ ra.

+ Sau nhiều thay đổi thì chuyển vào kho bằng lệnh:

        git commit -am "miêu tả thay đổi"

    hoặc

        git add *
        git commit -m "miêu tả thay đổi"

    hoặc

        git add <tên tập tin>
        git commit -m "miêu tả thay đổi"

    rồi dùng:

        git push --set-upstream origin <tên chi nhánh>

+ Để đưa chi nhánh mới vào kho trên mạng. Nếu đã có rồi thì chỉ cần:

        git push

+ Đưa các thay đổi ở chi nhánh vào `master` (Có thể ghi các lệnh vào một tập lệnh ở thư mục `$HOME/bin` và đánh dấu nó là khả thi hành `chmod u+x <tên tập tin>`):

        cd $BLENDER_MAN_EN
        git checkout master
        git pull https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git <tên chi nhánh>
        git add *
        git commit -m "Cập nhật thay đổi từ chi nhánh sang master."
        git push
        git checkout <tên chi nhánh>

+ Lấy nội dung của một chi nhánh đã tồn tại trên mạng:

        git clone -b <tên chi nhánh> https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git

+ Xóa chi nhánh:

        git branch -d <tên chi nhánh>

    nếu chi nhánh đã hoàn toàn hội nhập với chi nhánh ở kho trên mạng.

        git branch -D <tên chi nhánh>

    không cần biết là chi nhánh đã hội nhập với kho trên mạng hay không, ép buộc xóa.


------------------

## Dịch các bản PO (Translating PO files)

- Dùng một trình biên soạn văn bản có hỗ trợ định dạng phiên dịch **.po**, như bản **Kate** hoặc **Kwrite**. Trên Windows thì bạn còn có thể tự tạo cho mình một bản định nghĩa định dạng PO nữa, nếu sử dụng [NotePad++](https://notepad-plus-plus.org/). Có mấy từ chìa khóa (keywords):

    + **fuzzy**
    + **msgctxt**
    + **msgid**
    + **msgstr**

- Tìm hiểu thêm về [Định dạng của tập tin PO -- The Format of PO Files](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).
Trong đó:

    + `#, fuzzy` (**mập mờ**): Nếu dòng có dấu này thì máy phiên dịch sẽ không sử dụng nội dung ở dòng **msgstr** và coi nó như là *không có phiên dịch* hoặc *phiên dịch bị lỗi thời*, *phiên dịch có khả nghi về tính chính xác*. Chỉ xóa dòng này đi khi nào bản dịch là hoàn toàn đúng với bản tiếng Anh. Thêm dòng này vào phía trên dòng cho `msgid` nếu thấy phần phiên dịch là **mập mờ**, đáng khả nghi. Thông thường thì các dòng bắt đầu với ký tự **#** sẽ được coi là dòng *comment* và sẽ bị trình biên dịch bỏ qua.

    + `msgctxt` : Dòng đề **ngữ cảnh** sử dụng. Nếu sử dụng mã Python để thanh lọc **Message.id** (ví dụ, sử dụng **sphynx_int** để đọc nội dung của các bản **.po**, như ví dụ dưới đây), và sau đó, chuyển các **Message** sang dạng **list** và dùng thao tác **sorted** để sắp xếp theo trật tự alphabet, hòng lùng tìm các **id** của các **Message** theo phương pháp **Binary Search** thì **ngữ cảnh** `msgctxt` phải là một phần của khóa lọc và khóa lùng tìm.

            from sphinx_intl import catalog as c
            ..
            po_messages = c.load_po(po_file)

    + `msgid`: Dòng nội dung tiếng Anh. Khi lùng tìm thì phải sử dụng cái này làm khóa chính. Nhớ là khóa này có thể lặp lại. Phải kết hợp với **msgctxt** để tạo khóa duy nhất.
    + `msgstr`: Dòng nội dung trong tiếng Việt (dòng để dịch)

- Các dòng **Comment** luôn luôn khởi đầu bằng ký tự **#**. Các dòng này chỉ có tác dụng trong biên soạn để báo cho mình biết dòng chữ trong **msgid** được tìm thấy ở đâu trong mã nguồn, hoặc trong bản **rst**, và ở ngữ cảnh hoặc dòng nào mà thôi, nó sẽ bị bỏ đi trong quá trình biên dịch.

- Khi dịch thì chớ làm gì thay đổi dòng tiếng Anh, dòng `msgid`. Vì dòng chữ này đã được "bẻ gãy" (xuống dòng) với độ dài tối đa (76 ký tự), lúc sao chép nó vào bộ nhớ để dán lên trang [Google Translate](https://translate.google.com/#view=home&op=translate&sl=en&tl=vi) <a id="google-machine-translation"></a> thì các dấu ngoặc kép `"` có thể gây cản trở cho máy dịch và việc xóa chúng đi có thể là quá phiền toái, bạn nên đánh dòng lệnh sau:

        make gettext

    và vào thư mục **build** để thấy thư mục **locale**. Trong thư mục này sẽ có những tập tin với đuôi **.pot**. Các dòng **msgid** trong tập tin này là một dòng liên tục, không bị xuống dòng. Dùng một thực thể của trình biên soạn văn bản và bật xem văn bản **.pot** tương ứng với tập **.po**, sao chép (Ctrl+C) các dòng **msgid** vào bộ nhớ, trước khi dán (Ctrl+V) vào trang của [Google Translate](https://translate.google.com/#view=home&op=translate&sl=en&tl=vi), phần bên trái dành cho tiếng Anh, và lấy phần phiên dịch ở bên phải để đưa vào dòng **msgstr**, rồi sửa lại các từ nó viết sai và cách đặt câu cú, tránh sao cho quá dập khuôn tiếng Anh để người Việt đọc và cảm thấy quen thuộc. Một số nguồn đối chiếu sau mình có thể sử dụng được trong khi tra cứu và làm việc:

    + [Blender 3D: Noob to Pro](https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro)
    + [Blender 2.80 Reference Manual](https://docs.blender.org/manual/en/dev/getting_started/index.html)
    + [Blender Documentation](https://docs.blender.org/api/blender_python_api_master/info_quickstart.html)
    + [Developer Documentation](https://wiki.blender.org/wiki/Main_Page)
    + [Bản Phiên Dịch Giao Diện Người Dùng VI.PO](https://svn.blender.org/svnroot/bf-translations/trunk/po/vi.po)
        - nhớ đổi 'Text Encoding' (Chế độ Giải/Mã Hóa Văn Bản) của trình duyệt mạng sang 'Unicode' hoặc 'UTF-8' để xem được tiếng Việt có dấu. Trong trình duyệt mạng [Firefox](https://ftp.mozilla.org/pub/firefox/releases/) -- vào thư mục của bản có số phiên bản cao mà lấy cho mình một bản -- cho phép mình đổi chế độ giải mã (Bấm chuột phải ở thanh tiêu đề và chọn bật `Menu` lên, rồi vào `View ‣ Text Encoding ‣ Unicode`)
    + [Bảng Chú Giải Thuật Ngữ -- Glossary](https://docs.blender.org/manual/vi/dev/glossary/index.html)
    + [Youtube - Blender](https://www.youtube.com/user/BlenderFoundation)
    + [Từ Điển: Wiktionary tiếng Việt](https://vi.wiktionary.org/wiki/Trang_Ch%C3%ADnh)
    + [Từ Điển: Soha Tra Từ](http://tratu.soha.vn/)

------------------

## Biên tập và xử lý hậu kỳ các thay đổi (Compiling and post processing changes)

+ Các tập tin mới được tạo sẽ chứa một số từ cần điền cho tác giả và ngày sửa đổi v.v. Nếu bạn cảm thấy công việc thay thế chúng lặp đi lặp lại, tẻ nhạt, thì hãy sử dụng tập lệnh

        change_placeholders.sh

    trong thư mục nhánh

        blender_docs/toos_maintenance

+ Sao lấy một bản vào thư mục **bin** địa phương của bạn và thay tất cả các giá trị đề cập trong tập tin với các chi tiết cụ thể của mình, rồi sau mỗi lần thay đổi một tập tin phiên dịch, bạn nên thực hiện các lệnh sau:

        $HOME/bin/change_placeholders.sh $BLENDER_MAN_VI
        make -d --trace -w -B -e SPHINXOPTS="-D language='vi'" 2>&1

+ Xem các thay đổi ở địa phương bằng cách dùng trình duyệt mạng, vào thư mục

        $BLENDER_MAN_EN/build/html/index.html

+ Nên lưu địa chỉ này vào mục ưa thích (Favorites) (Ctrl+D) của trình duyệt mạng để lần sau cứ vào đấy bấm vào để xem trang đầu, F5 (làm tươi lại - refresh) để lấy các thay đổi gần đây nhất mà không phải mở lại


### Nhập kho các thay đổi (Committing changes to repository)

+ Khi thay đổi xong và muốn nhập kho thì làm như sau:

    1. Xem các thay đổi:

            git status

    2. Nhập kho vào ổ địa phương:

        + Báo cho git biết là không ký lần nhập kho bằng mật mã riêng của cá nhân. Chỉ làm một lần.

                git config commit.gpgsign false

        + Báo cho git là lưu trữ tên người dùng và mật mã, dùng cho những lần sau. Chỉ làm một lần.

                git config credential.helper store

+ Đưa vào kho địa phương ở máy

        git commit -am "<ghi chú về những gì đã làm trong thay đổi vừa rồi>"

+ Chuyển giao các thay đổi vào kho trên mạng

        git push

### Cập nhật các thay đổi ở chi nhánh chính **master**

+ Lấy các thay đổi ở tất cả các chi nhánh trên mạng về máy mình, sử dụng:

        git pull --all

+ Sau mỗi lần `git commit` thì thi hành `git pull` để hội nhập các thay đổi ở máy chủ trên mạng với máy mình.

------------------

## Các tập lệnh có thể cần sử dụng (Favourable scripts)

Trong khi làm việc, việc tái thi hành lệnh đã làm trước đây sẽ là một việc không tránh khỏi, chẳng hạn như lệnh tạo *html*. Tốt nhất là kèm chúng vào một tập lệnh ở thư mục **bin** địa phương và đặt nó là có quyền thi hành:

1. Tập lệnh *Python* - **makevidoc.py**:

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



    + Lưu tập lệnh `makevidoc.py` này vào thư mục **\$HOME/bin** của máy. Nếu thư mục này chưa có thì làm theo các lệnh sau: (Có thể thay **\$HOME** sang **\$WIN_HOME** để có thể biên soạn các tập lệnh bằng các trình biên soạn văn bản của riêng mình một cách dễ dàng.)

            cd $HOME
            mkdir bin

    + Nhớ biên soạn bản `·bashrc` và đặt dòng sau để thư mục **\$HOME/bin** nằm trong danh sách các đường dẫn mà hệ điều hành sẽ lùng tìm các bản tập lệnh khi chạy dòng lệnh:

            export MYBIN=$HOME/bin
            export PATH=$MYBIN:$PATH


    + Đặt tập lệnh này là **Khả Thi Hành** (executable) bằng lệnh:

            chmod u+x $HOME/bin/makevidoc.py

    + Sau đó, chúng ta có thể chạy nó như các ví dụ sau:


        - Xem hướng dẫn sử dụng

                makevidoc.py --help

        - Thi hành *make* nhưng không xóa bản cũ đi, viết đè lên. Phương pháp này sẽ nhanh hơn, song nhiều khi sẽ không cho kết quả chính xác:

                makevidoc.py

        - Thi hành *make* và xóa bản cũ đi:

                makevidoc.py -c

        - Thi hành **make** và xóa bản cũ đi, định thư mục nơi nó cần làm việc là thư mục hiện tại ($PWD = Print Working Directory: In ra thư mục làm việc):

                makevidoc.py -c $PWD

2. Tập lệnh **change_placeholders.sh**

    + Tập lệnh này nằm trong thư mục:

            blender_docs/toos_maintenance


        + Sao lấy một bản vào thư mục **\$HOME/bin** của mình và đặt tập lệnh thành **Khả Thi Hành** (executable) như nói ở trên.

        + Tập lệnh này cho phép mình điền tên và e-mail của mình vào phần *COMMENT* của các văn bản mà mình sửa, đồng thời điền ngày giờ mình đã làm nữa. Nó dùng lệnh `svn` và `git` để tìm các văn bản có đuôi là `.po` đã thay đổi. Nếu phải tự lùng tìm ở một thư mục nào đó không phải là thư mục có thư mục `.svn` hoặc `.git` thì nó sẽ tìm các văn bản có đuôi là `.po` mà thôi và cách này là cách làm việc lâu nhất.

        + Các từ mình cần điền chi tiết của cá nhân là:

                YOUR_NAME="Họ tên đầy đủ"
                YOUR_EMAIL="địa-chỉ-email@máy_chủ.com"


        + Tập lệnh này thường được thi hành trong những trường hợp mà các văn bản **.po** bị thay đổi do:
            * Bản thân mình biên soạn nó
            * Sau khi thi hành lệnh

                    make update_po


            để cập nhất các thay đổi từ bản tiếng Anh sang, và quá trình này, ngoài việc cập nhật các thay đổi từ các tập tin nguồn `~/blender_docs/manual/*.rst`, nó còn đánh dấu (không xóa đi) những phần văn bản đã bị xóa đi trong bản nguồn, bằng cách đánh dấu các dòng này với tiền tố **\#~**. Tập lệnh **change_placeholders.sh** cũng phát hiện cái này và xóa các dòng có tiền tố **\#~** ra khỏi văn bản **.po**.


3. Các dòng lệnh mình đã đánh trong cửa sổ dòng lệnh được trình xử lý dòng lệnh ghi lại và trong khi làm việc trong cửa sổ dòng lệnh mình có thể

    + Dùng các phim mũi tên *lên*, *xuống* để gọi lại các dòng lệnh đã đánh theo tuần tự. Mũi tên trái/phải sẽ quay trở lại/tiến về trước các ký tự dòng lệnh, `Home` để về đầu dòng, `End` để về cuối dòng, `Backspace`/`Delete` để xóa về trước hoặc sau. `Insert` để đổi chế độ viết đè lên ký tự cũ, hoặc chèn thêm và vị trí con trỏ. Dùng các phím cơ bản này mình có thể gọi lại các dòng lệnh cũ, biên soạn chúng để thi hành lệnh mới với các tham số khác nhau.

    + Lệnh **history** (Lịch Sử) liệt kê lại các lện đã từng đánh và được ghi lại. Số dòng được định trong tập **.bashrc**

            # for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
            HISTSIZE=1000
            HISTFILESIZE=2000


    + Khi số dòng vượt quá hạn định này thì tất cả những dòng lịch sử trước sẽ bị xóa đi và những dòng mới sẽ được bắt đầu lại từ đầu. Nếu có những dòng lệnh đánh mà mình muốn lưu lại vào một tập tin khác thì mình có thể thi hành các lệnh sau - đặt tên cho tập lệnh là `savehistory.sh`:

            #!/bin/bash
            histfile=$HOME/Documents/my_history.txt
            tempfile=$HOME/tmp.txt
            history >> $histfile
            cat $histfile | sort -nu > $tempfile
            mv $tempfile $histfile


    + Nhớ lệnh **sort** có hai tham số:

            -n : numerical, tức so sánh trong khi sắp xếp dùng giá trị số của dòng, hay lấy thứ tự những con số dẫn đầu, tức số dòng.
            -u : unique, xóa đi những dòng hoàn toàn giống nhau, chỉ giữ lại một dòng.


        xem thêm hướng dẫn về lệnh **sort** dùng:

            man sort


        vì lệnh này sắp xếp cách dòng lệnh theo con số dẫn đầu (số của dòng) (tham số **-n** của lệnh **sort**) và khi HISTSIZE > 1000, nó quay trở lại số 1 thì trật tự sẽ không còn nằm ở dưới, theo tuần tự thời gian mà mình nghĩ là nó sẽ nằm nữa.

    - Khi lệnh **history** (Lịch Sử) liệt kê các dòng lệnh, nó còn liệt kê dòng số ở đầu. Mình có thể gọi lại dòng lệnh bằng cách điền con số dòng với dấu chấm than đứng trước, như sau:

            !<số dòng>
            !123


        và bấm 'Enter'. Lệnh ở dòng số này sẽ được thực hiện (ví dụ thi hành lại lệnh ở dòng số 123)


4. Tập lệnh **.bash_aliases** (Biệt danh)

    - Tập lệnh này sẽ được thi hành bởi tập tin `.bashrc`, nên khi nạp lại tập tin `.bashrc` bằng lệnh `. .~/.bashrc` thì các lệnh biệt danh (viết tắt) cũng sẽ được nạp vào bộ nhớ. Điều tra các lệnh viết tắt bằng cách đánh:

            alias

        và bấm `Enter` để thấy các lệnh được liệt kê.

    - Biên soạn tập tin này để cho các tên viết tắt của các lệnh, chẳng hạn:

            alias graph="git log --all --decorate --oneline --graph"
            alias ll='ls -alF'

        để khi ở dòng lệnh chỉ cần đánh:

            graph
            ll

        thay vì phải đánh toàn bộ.


------------------

## Chuyển thư mục `/home` sang một ổ cứng ngoài

Việc tách riêng hệ điều hành và thư mục $HOME của mình là một thực hành khá tốt, vì khi có vấn đề, hoặc phải cài lại hệ điều hành, thì mình không cần phải lo đến việc cài đặt lại các thông tin ở $HOME của mình. Chỉ việc cài lại hệ điều hành và lắp ổ cứng $HOME vào là có thể làm việc ngay được. Ví dụ sau làm trên hệ điều hành Linux Mint 18.04:

### Cài đặt Linux Mint 18.04:

- Mua lấy một ổ cứng SSD chừng 128GB là thừa đủ. Cũng cần có một ổ cứng ngoài - có thể sử dụng lại ổ cứng cũ nếu không muốn tốn tiền, và sử dụng nó làm ngăn $HOME của riêng mình, cỡ chừng 1TB-4TB.

- Hoặc là dùng một đĩa DVD trắng, hoặc là một thẻ USB, chừng 2GB là đủ

- Vào trang của [Linux Mint](https://linuxmint.com/download.php) và lấy cho mình một bản. Chọn cái xứng hợp với máy của mình. Nếu máy là 64bit thì chọn lấy cái 64bit. Nếu máy vẫn còn là 32bit thì lấy bản dành cho 32bit.

- Tốt nhất là đặt mua đĩa tại [osdisc.com](https://www.osdisc.com/products/linux/linuxmint?affiliate=linuxmint). Giá 1 DVD là $5.95 (Đô-la Mỹ). Tôi chưa đặt qua nên không biết giá cước chuyển về Việt Nam là bao nhiêu. Ở Anh, tôi chỉ mua tạp chí [Linux Magazine](http://www.linux-magazine.com) ở cửa hàng bán báo chí là có cả đĩa kèm theo, song phải nhắm đúng tháng nó in ra đĩa mình mong muốn.

- Nếu định thử phương pháp dùng thẻ USB và máy hiện tại đang sử dụng Windows thì vào [đây](https://sourceforge.net/projects/win32diskimager/files/Archive/Win32DiskImager-1.0.0-binary.zip/download) lấy một bản xuống máy để dùng nó viết tập tin bản Linux Mint mình vừa lấy xuống. Phương pháp an toàn nhất vẫn là sử dụng đĩa DVD mua, tuy chậm hơn.

- Sau khi viết xong thì dùng thẻ USB, hoặc đĩa DVD mà mình đã viết bản Linux Mint lên đó rồi để khởi động máy. Nhớ kiểm tra BIOS của máy để cho phép nó khởi động dùng thẻ USB trước tiên, trước khi chạy ổ cứng.

- Sau khi khởi động, nếu sử dụng ổ đĩa mà mình định sử dụng đã có thông tin ở trong đĩa rồi, thì nên xóa đi bằng cách sau:
    - Bấm tổ hợp phím `Ctrl-Alt F1` để chuyển sang chế độ dòng lệnh.
    - Điền người dùng mặc định là `mint`.
    - Bấm Enter ở dòng hỏi `password:`, không có mật mã.
    - Điền `sudo -s` và bấm `Enter` để vào chế độ người quản lý hệ thống (Administrator, Linux gọi là `root`).
    - Thi hành các dòng lệnh sau:

    1. Liệt kê các ổ cứng, xem cái mình sẽ xóa đi và cài hệ điều hành vào là cái nào, bằng lệnh:

            fdisk -l


        Để ý tên thường là `/dev/sda` hoặc `/dev/sdb` v.v. Ghi nhớ cỡ của ổ cứng để phát hiện cho đúng. Ổ cứng thường có cỡ lớn hơn đĩa và thẻ USB rất nhiều. Nhớ đơn vị cỡ TB (Terabyte) = 1024 GB (Gigabyte), GB = 1024 MB (Megabyte), MB = 1024 KB (Kilobyte), KB = 1024 B (Byte). Giả dụ, ổ đĩa của chúng ta được hệ điều hành gán vào `/dev/sdb', thi hành lệnh:

    2. Xóa các rãnh của ổ cứng cũ. Ví dụ này chỉ xóa 1GB đầu tiên:

            dd if=/dev/zero of=/dev/sdb bs=1G count=1

        để viết 1GB dữ liệu trống ra ổ cứng và xóa trắng 1GB mà thôi. Nếu muốn viết trắng toàn bộ ổ cứng thì viết:

            dd if=/dev/zero of=/dev/sdb bs=1G status=progress

        để xóa trắng tất cả, đưa giá trị của các rãnh về giá trị 0 (`/dev/zero`) và phần mềm sẽ thông báo cho mình biết là nó làm việc đến đâu rồi, cùng tốc độ viết (`status=progress`).

    3. Sau khi viết xong, thi hành:

            partprobe /dev/sdb

        để đọc lại cấu hình của ổ mà mình vừa xóa đi, vì cấu hình, sau khi đã xóa đi, không còn giống như cái cũ trước đây nữa.

    4. Bấm tổ hợp phím `Ctrl-Alt F7` để quay trở lại giao diện đồ họa. Bấm nút 'Install Linux Mint' trên mặt bàn làm việc (desktop) để khởi động cài đặt và điền các thông tin những hướng dẫn trên màn hình. Các bạn có thể chọn ngôn ngữ `tiếng Việt` ở vùng liệt kê danh sách ngôn ngữ trong cửa sổ bên trái và bấm nút `tiếp tục` để thi hành. Theo kinh nghiệm cá nhân, các bạn nên cài bằng tiếng Anh, rồi sau này cài thêm `ibus-unikey` và dùng `ibus` để đánh tiếng Việt thì hơn.


### Cài ổ cứng riêng biệt cho phần $HOME

+ Sau khi cài đặt xong khởi động lại, cắm ổ sẽ dùng để làm $HOME vào.
+ Nếu ổ cứng mình là một ổ cũ và sử dụng hệ thống tập tin khác với những cái thuộc Linux, như `ext4`, thì nên sử dụng phần mềm `disks` (Đĩa) để định dạng (format) nó.

+ Khi đã đăng nhập thì bật `Terminal` lên và thi hành các lệnh sau:

        sudo fsdisk -l

    để vào chế độ người quản lý hệ thống và xem các ổ cứng, nhất là ổ dùng để làm $HOME gọi là gì.

+ Nếu ổ cứng chưa được chuẩn bị thì sử dụng công cụ `disks` để định dạng (format) nó. Nên sử dụng hệ thống tập tin `ext4` (mặc định của Linux) thì hơn. Nhớ để ý chỉ danh `/dev/sd?` xem hệ điều hành gán cho nó là ổ gì. Các đơn giản với các ổ USB là bật `disks` lên và rút ổ ra/cắm ổ vào và xem sự thay đổi của danh sách.

    - Ví dụ, liệt kê ổ cứng:

            sudo fdisk -l
            [sudo] password for <username>:

                Disk /dev/sda: 111.8 GiB, 120034123264 bytes, 234441647 sectors
                Units: sectors of 1 * 512 = 512 bytes
                Sector size (logical/physical): 512 bytes / 512 bytes
                I/O size (minimum/optimal): 512 bytes / 512 bytes

    - Biên soạn đĩa bằng lệnh `fsdisk`:

            sudo fdisk /dev/sda

                Welcome to fdisk (util-linux 2.31.1).
                Changes will remain in memory only, until you decide to write them.
                Be careful before using the write command.

                Device does not contain a recognised partition table.
                Created a new DOS disklabel with disk identifier 0xe7e87b15.

    - In thông tin bằng lệnh `p` (Print):

            Command (m for help): p

                Disk /dev/sda: 111.8 GiB, 120034123264 bytes, 234441647 sectors
                Units: sectors of 1 * 512 = 512 bytes
                Sector size (logical/physical): 512 bytes / 512 bytes
                I/O size (minimum/optimal): 512 bytes / 512 bytes
                Disklabel type: dos
                Disk identifier: 0xe7e87b15

    - Kiến tạo phần ổ cứng mới bằng lệnh `n` (New):

            Command (m for help): n
                Partition type
                p   primary (0 primary, 0 extended, 4 free)
                e   extended (container for logical partitions)
                Select (default p): p (Chọn primary)
                Partition number (1-4, default 1):
                First sector (2048-234441646, default 2048):
                Last sector, +sectors or +size{K,M,G,T,P} (2048-234441646, default 234441646):
                Created a new partition 1 of type 'Linux' and of size 111.8 GiB.

    - Viết ra ổ cứng những thay đổi đã làm:

            Command (m for help): w
                The partition table has been altered.
                Calling ioctl() to re-read partition table.
                Synching disks.


    - Định dạng hệ thống tập tin cho phần ổ cứng vừa tạo sử dụng sắp đặt mặc định, để ý UUID (Universally Unique Identifier) mà hệ điều hành gán cho nó:

```bash
            sudo mke2fs -t ext4 /dev/sda1

                mke2fs 1.44.1 (24-Mar-2018)

                Creating filesystem with 29304949 4k blocks and 7331840 inodes
                Filesystem UUID: f98b7efa-08fd-40a2-8f6d-94388c453b0d
                Superblock backups stored on blocks:
                    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
                    4096000, 7962624, 11239424, 20480000, 23887872

                Allocating group tables: done
                Writing inode tables: done
                Creating journal (131072 blocks): done
                Writing superblocks and filesystem accounting information: done
```

+ Để liệt kê các thông tin này dùng lệnh

        sudo blkid /dev/sda1
            /dev/sda1: UUID="f98b7efa-08fd-40a2-8f6d-94388c453b0d"  TYPE="ext4"

+ Đổi nhãn hiệu để dễ nhận biết hơn bằng lệnh:

        sudo e2label /dev/sda1 "MY_HOME"

+ Sao chép dòng thông tin về ổ mà mình sẽ sử dụng, chẳng hạn như `/dev/sdc1` ở trên.

+ Tạm thời vào địa chỉ của ổ cứng, xem điểm `mount` ở đâu. Nếu dùng `disks` thì bấm nút mũi tên đen bên dưới để `mount` nó và xem điểm `mount` là ở đâu. Thường là

+ Biên soạn `/etc/fstab` để đưa thông tin này vào đó, đặt ánh xạ sang ổ `/home` cho nó như sau:

        nano /etc/fstab

    và điền dòng sau vào cuối cùng:

        UUID=d21aebfe-716e-11e2-97f7-001a64633f00   /home   ext4    defaults    0   2

    nhớ xóa các ngoặc kép ở giá trị của `UUID`

------------------

## Một số phương pháp có thể sử dụng để tăng hiệu suất làm việc

### Dùng máy phiên dịch Google

Cái này đã nói đến ở [trên](#google-machine-translation) rồi, vào trang [Google Translate](https://translate.google.com/#view=home&op=translate&sl=en&tl=vi) và thi hành làm như hướng dẫn

### Tăng lượng dòng định nghĩa từ gõ tắt trong bản macro của Unikey

+ Bản ibus-unikey ở kho lấy về có một giới hạn về số từ viết tắt trong bảng macro có thể ghi và nạp vào bộ nhớ là 1024 dòng, mỗi dòng là một định nghĩa. Tôi có viết thư cho anh Lê Quốc Tuấn, chủ nhân của phần mềm này, và làm theo sự hướng dẫn của anh, [vào đây](https://github.com/vn-input/ibus-unikey) lấy bản mã nguồn dùng lệnh:

        sudo apt-get install -y cmake g++ make pkg-config libibus-1.0-dev libgtk-3-dev
        cd $HOME
        mkdir sources/
        cd sources
        git clone https://github.com/vn-input/ibus-unikey.git
        cd ibus-unikey
        kwrite ukengine/keycons.h

+ Đổi dòng:

        #define MAX_MACRO_ITEMS 1024

    thành

        #define MAX_MACRO_ITEMS 1024 * 4

    Tức tăng số dòng macro có thể sử dụng lên thành 4 lần (4096 dòng). Lưu thay đổi và quay trở lại dòng lệnh:

        mkdir build
        cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=release -DLIBEXECDIR=/usr /lib/ibus ..
        make
        sudo make install

+ Bấm chuột phải ở biểu tượng Unikey trên thanh tác vụ và chọn 'Restart' để tắt bản cũ đi, lấy bản mới vào bộ nhớ. Hoặc là biên soạn bản 'macro.txt' và cho thêm từ vào đó, rồi 'Import' nó vào hoặc 'import' từ một bản định nghĩa khác đã có vào. Sau khi 'Save' (Lưu) thì có thể vào thư mục '$HOME/.ibus/unikey' và kiểm tra số dòng của bản 'macro' trong đó, bằng

        cat macro | wc -l

    hoặc dùng:

        kwrite macro

    và kiểm tra số dòng mà phần mềm đã ghi. Hơn 1024 là được.

+ Nhớ mỗi lần thay đổi nội dung của 'macro' trong bộ nhớ thì phải dùng phím chuyển ngôn ngữ (giữa tiếng Anh và tiếng Việt) để đổi sang tiếng Anh rồi quay trở lại tiếng Việt, để kích hoạt bản định nghĩa macro mới.

+ Cách biến quá trình nhập các 'macro' mới vào

        .ibus/unikey/macro

    và khởi động lại **ibus-engine-unikey** tự động, sau mỗi lần thay đổi, hoặc điền thêm định nghĩa vào, dùng **kate** hoặc **kwrite**, viết một bản mã **bash shell**, tương tự như sau đây và đặt tên cho nó là **refresh_unikey.sh**, chẳng hạn. Ví dụ này sắp đặt bản **macro.txt** nằm trong thư mục *~/Documents*:

        #!/bin/bash
        pkill -9 ibus-engine-uni
        cp -a ~/Documents/macro.txt ~/.ibus/unikey/macro
        chmod 664 ~/.ibus/unikey/macro
        /usr/ibus-engine-unikey --ibus &

    nhớ đổi chế độ cho bản **refresh_unikey.sh** sang bao gồm quyền thi hành, bằng dòng lệnh

        chmod u+x refresh_unikey.sh

    Nhớ là sau khi chạy lệnh **refresh_unikey.sh** ở dòng lệnh thì phải bấm `Ctrl+Spacebar` hai lần đề nó chuyển sang tiếng Anh, rồi tiếng Việt. Cách làm này sẽ giảm thiểu việc chúng ta phải vào trình đơn và dùng lệnh **import**.


### Sử dụng microphone và chức năng dịch giọng nói đánh thành chữ của Google

Chức năng này trong bản 'chromium' - bản nguồn mở - lấy ở kho không hoạt động, tuy hình microphone xuất hiện, song khi bấm vào đó thì nó sẽ nói 'no internet connection' và cho dù mình sửa đổi sắp đặt trong mục

    Settings ‣ Advanced ‣ Privacy and security ‣ Content settings ‣ Microphone

và chọn 'Built-in Audio Analogue Stero' đi chăng nữa.

Chúng ta phải cài đặt 'Chrome' bản chính, như hướng dẫn [ở đây](https://www.tecmint.com/install-google-chrome-in-debian-ubuntu-linux-mint/),

1. Cách thứ nhất là:

        cd Downloads
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
        sudo apt-get update
        sudo apt-get install google-chrome-stable

2. Cách thứ hai là:

        cd Downloads
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo dpkg -i google-chrome-stable_current_amd64.deb

    + Sau đó vào trình đơn 'Internet' của hệ điều hành và bấm thi hành 'Google Chrome' hoặc khởi động nó từ dòng lệnh:

            google-chrome-stable &

    + Bấm vào nút ba chấm ở bên phải của dòng địa chỉ, sát mép cửa sổ và vào thư mục:

            Settings ‣ Advanced ‣ Privacy and security ‣ Content settings ‣ Microphone

        bật nút 'Block' (Ngăn chặn) để nó chuyển thành 'Ask before accessing (recommended)' (Hỏi trước khi truy cập (đề cử))

    + Nếu máy có nhiều microphone thì có thể bấm vào nút ở đó và chọn cái mình muốn sử dụng.

    + Bật một 'Tab' mới (bấm dấu '+' ở trên cùng, hoặc bấm 'Ctrl+T'), và bấm vào nút hình cái microphone ở bên phải ở dòng đề 'Search Google or type a URL' (Tìm kiếm Google hoặc đánh máy chữ một dòng địa chỉ URL). Hình biểu tượng microphone màu đỏ hiện ra và bên trái dòng chữ chuyển từ 'Speak now..' (Nói đi) sang 'Listening' (đang lắng nghe). Nói một vài chữ tiếng Anh như 'Hello', hoặc 'Thank you', để nó tìm cho mình. Mình sẽ thấy các chữ ấy được sử dụng để tìm các trang và phim ảnh liên quan đến các chữ mình nói.

    + Lần đến trang [Trình biên soạn văn bản của Google trên mạng](https://docs.google.com/document) và bấm vào nút dấu cộng '+' để lấy một bản tài liệu mới. Bấm vào

            File ‣ Language ‣ Tiếng Việt

        để nó luôn luôn sử dụng tiếng Việt trong khi phiên dịch. Bấm vào nút 'Tools' (Các Công cụ) ở trình đơn và chọn 'Voice typing' (Đánh máy chữ bằng giọng nói). Hình biểu tượng cái microphone sẽ hiện ra ở bên trái lề. Nếu thấy nút ở trên hình cái microphone vẫn còn đề là 'English' thì bấm vào đó và chọn đổi sang 'Tiếng Việt' để đổi ngôn ngữ nó lắng nghe và phiên dịch. Phần mềm sẽ tự lưu các sắp đặt và nội dung của bản tài liệu mình đang sử dụng, lần sau, khi sử dụng lại thì nó sẽ nhớ là mình sử dụng tiếng Việt. Nhớ lưu lại dòng liên kết (Ctrl+D) và ghi nó vào một thư mục nào đó trong trình đơn Những Ưa Thích (*Favorites*) của mình, để lần sau, mình sử dụng lại thì chỉ cần bấm vào dòng liên kết là đến lại được.

    + Dùng 'Kate' hoặc 'Kwrite' bật một bản dịch mình muốn làm. Xem dòng **msgid** và dịch nhẩm trong đầu, rồi bấm vào nút hình cái microphone (hiện lên màu đỏ) ở trang của [Trình biên soạn văn bản của Google trên mạng](https://docs.google.com/document) và nói dòng đã dịch trong đầu ấy. Nó sẽ đánh ra các chữ mà nó nghĩ là đúng. Sau khi đã nói xong thì bấm vào hình biểu tượng cái microphone và tắt nó đi (màu đen).

    + Nếu cần phải đánh lại một chữ nào thì bấm và chọn chữ ấy (màu xanh dương), rồi nói lại chữ nó đánh sai. Gợi ý, để nó hiểu được những chữ khó, đôi khi phải nói vài từ trong ngữ cảnh đó, chẳng hạn, thay vì chỉ nó 'lý', thì nói 'lý thuyết' hoặc 'lý luận', hoặc để được chữ 'xương', thay vì 'sương' thì nói 'xương lợn', thay vì 'hạt sương'.

    + Dùng chuột quét để chọn và chép (Ctrl+C) nó vào bộ nhớ của máy. Chuyển sang bản mình đang dịch và bấm (Ctrl+V) để dán dòng chữ đã dịch vào. Sửa lại thành kiểu chữ thường hoặc hoa như mình muốn.

###Sử dụng Python để viết lập trình
+ Vì lượng thông tin trong các tài liệu là khá lớn và có thể có nhiều việc nhắc lại, tức là những việc mình có thể tự động hóa bằng lập trình, đồng thời tái sử dụng các chức năng của mã nguồn 'sphynx', mã nguồn được viết trong Python, nữa. Sau khi cài đặt xong thì mã này sẽ nằm trong thư mục:

        /home/htran/.local/bin

    nơi mà các bản thi hành được nằm, và thư mục:

        /home/htran/.local/lib

    nơi các bản thư viện nằm.

+ Để khỏi phải lo lắng quá nhiều về mã văn bản UTF-8, mã tiếng Việt sử dụng, thì chúng ta nên chuyển Python sang sử dụng **python3**, như đã nhắc đến [ở đây](#cai-at-cac-phan-mem-can-thiet-cho-viec-bien-tap-install-softwares-necessary-for-compilation).

+ Theo mặc định thì bản **.profile** ở thư mục *$HOME* của mình sẽ có dòng này:

        #set PATH so it includes user's private bin if it exists
        if [ -d "$HOME/.local/bin" ] ; then
            PATH="$HOME/.local/bin:$PATH"
        fi

    và do đó, nếu mình liệt kê biến môi trường **PATH** ra, bằng lệnh:

        echo $PATH

    thì mình sẽ thấy là địa chỉ **$HOME/.local/bin** sẽ được đặt trước tất cả những địa chỉ (thư mục) khác. Điều này có nghĩa là khi trình điều khiển môi trường (ví dụ `/bin/bash`) phiên dịch các dòng mã đánh ở bàn giao tiếp, nó sẽ lùng tìm ở thư mục **$HOME/.local/bin** trước, trước khi đi đến các thư mục khác được nói đến trong biến môi trường **PATH**.

    Nếu không, chúng ta có thể tự mình thêm vào bản **.profile** ở thư mục $HOME của mình, hoặc vào bản **.bashrc** của mình.

+ Kiểm tra xem đường dẫn đến các thư viện của hệ thống Python nằm ở đâu, bằng cách vào cửa sổ dòng lệnh và đánh các lệnh sau:

        python3
        Python 3.6.7 (default, Oct 22 2018, 11:32:17)
        [GCC 8.2.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import sys
        >>> sys.path

    Lệnh này sẽ liệt kê các thư mục mà Python3, khi hoạt động, sẽ lùng tìm các thư viện của nó. Mình có thể điều khiển cái này bằng 2 cách:

    - Điền vào dùng biến môi trường **PYTHONPATH**. Đặt cái này trong bản **.bashrc** của mình bằng dòng:

                export PYTHONPATH=$HOME/.local/lib/python3.6/site-packages

        xem thêm thông tin về các biến môi trường của Python [ở đây](https://docs.python.org/3/using/cmdline.html?#environment-variables)

    - Điền 2 dòng sau ở đầu bản mã lập trình của mình (*.py), trước khi dùng lệnh **import** hoặc **from <tên> import** :

                import sys
                sys.path.append("/home/<tên tài khoản người dùng>/.local/lib/python3.6/site-packages")

                from sphinx_intl import catalog as c

                ....
                po_doc = c.load_po(po_path)
                ....
                c.dump_po(po_path, po_doc)

        Nên nhớ, lệnh **c.dump_po** trong tập lệnh

                $HOME/.local/lib/python3.6/site-packages/sphinx_intl/catalog.py

                # Đề án phiên dịch bản hướng dẫn sử dụng Blender (_Blender Reference Manual_)

## Lấy bản ZIP mới nhất của bản hướng dẫn sử dụng hiện đang làm:

Có hai bản hiện được biên tập:

- Tất cả nội dung nằm trong [một tập tin index.html](blender_docs/build/blender_vietnamese_single.zip)
- Nội dung được phân ra [nhiều bản html, mỗi tập tin một đề mục riêng](blender_docs/build/blender_vietnamese_html.zip)

## Lấy bản phiên dịch giao diện *blender.mo* cho:
- Phiên bản [2.79](gui/2.79/locale/vi/LC_MESSAGES/blender.mo)
- Phiên bản [2.80](gui/2.80/locale/vi/LC_MESSAGES/blender.mo)
Lưu ý: Xin xem hướng dẫn ở địa chỉ cũ [này](https://github.com/hoangduytran/blender-internationalisation/blob/master/README.md) để xem cách cài đặt bản *blender.mo* vào thư mục của phần mềm Blender.

## Chuẩn bị (Preparations)

Tốt nhất là [cài đặt và sử dụng hệ điều hành Linux](https://www.youtube.com/watch?v=uzpKjeZykoQ&list=PL9LmhZmBx5yBIcEMwhVcLn7mtlGWW2HWu). Nếu không làm được thì học cài đặt Hệ Thống Phụ Linux (**WSL**) trên phiên bản Windows 10. Phương pháp  đã được ghi lại trên các trang này:

+ [Hướng dẫn cài đặt trên Windows 10 -- Windows 10 Installation Guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10)

+ [Thủ công tải về máy các gói phân phối của WSL (Linux) -- Manually download WSL distro packages](https://docs.microsoft.com/en-us/windows/wsl/install-manual)

+ [Khởi thủy bản phân phối vừa cài đặt xong -- Initializing a newly installed distro](https://docs.microsoft.com/en-us/windows/wsl/initialize-distro)

Điều này sẽ cho phép bạn truy cập vào tính năng phong phú mà môi trường dòng lệnh Linux cung cấp.


## Kiểm tra phiên bản Linux hiện có (Find the current release's version)

Trước tiên, hãy kiểm tra phiên bản Linux có sẵn tại trang web phân phối. Trong ví dụ này, chúng tôi đã chọn **Ubuntu Desktop 18.04**. Bạn có thể tìm hiểu thêm về phiên bản mới nhất [tại đây](https://www.ubuntu.com/download/desktop)

## Cài đặt hệ thống phụ Linux (Setup the Linux subsystem)

Có thể cách tốt hơn là cài đặt bằng cách sử dụng *PowerShell*. Mở *PowerShell* bằng cách nhập tên vào hộp tìm kiếm *Cortana*. Nhấp chuột phải vào mục *PowerShell* tìm thấy và chọn thi hành với tư cách *Quản trị viên* (run as Administrator). Điều đầu tiên, chúng ta cần kích hoạt hệ thống phụ Linux, sử dụng dòng lệnh sau:

        Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

Khi làm xong, tắt nguồn và khởi động lại hệ thống là điều bắt buộc, vì vậy, hãy khởi động lại hệ thống. Khi hệ thống được bật trở lại, hãy quay lại *PowerShell* và nhập lệnh sau:

        Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu.appx -UseBasicParsing

Việc làm này sẽ tải xuống *Linux Ubuntu* và lưu trữ trong tập tin `Ubuntu.appx` tại thư mục làm việc hiện tại, như được chỉ rõ trong tham số `-OutFile`. Bạn có thể chọn di chuyển nó sang thư mục khác sau khi tải xuống hoàn tất, bằng cách thực hiện:

```bash
  mv Ubuntu.appx 'c:\Users\<your username>\Downloads'
```

Khi tập tin `Ubuntu.appx` đã được lấy xuống, sử dụng *Explorer* và xem thư mục lấy xuống, đảm bảo rằng tập tin nằm ở đó, sau đó nhấp đúp vào `Ubuntu.appx` để chạy cài đặt, nhập tên người dùng, và mật khẩu, cộng với xác minh mật khẩu cho tài khoản người dùng như được hiển thị trong cửa sổ dòng lệnh.

Khi quá trình cài đặt hoàn tất, bạn có thể tìm thấy biểu tượng của *Ubuntu* trong *Start Menu* (nút trình đơn *Bắt Đầu*), hoặc tìm kiếm trong *Cortana*, bằng cách gõ `Ubuntu` vào hộp tìm kiếm. Sau đó bạn có thể thực hiện một hoặc cả hai trong số những điều sau đây:

    Bấm chuột phải và chọn Ubuntu 18.04 ‣ Đính vào trình đơn bắt đầu (pin to start)
    Bấm chuột phải và chọn Ubuntu 18.04 ‣ thêm (more) ‣ Đính vào thanh tác vụ (pin to taskbar)

## Cập nhật hệ thống phụ Linux (Updating the Linux subsystem)

+ Bản mà bạn đã tải xuống và cài đặt có thể không phải là phiên bản mới nhất, vì vậy hãy chạy các lệnh sau để cập nhật môi trường:

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y git subversion

+ Bạn còn có thể tải xuống máy bản [Kate trên Windows](https://kate-editor.org/2016/01/28/kate-on-windows/) làm một trình biên soạn văn bản bổ sung, thay cho cái hiện tại đang sử dụng. Cái này cho phép nêu bật các chữ chìa khóa của tập tin **.po** phiên dịch, dễ làm việc hơn trên giao diện đồ họa.


## Lưu Ý (Note)

+ Vị trí của bản Ubuntu 18.04 nằm tại:

        C:\Users\<windows username>\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs\home\<Ubuntu's username>

    Mình có thể tìm thấy ánh xạ của ổ đĩa C: bằng cách sử dụng:

        mount

    và nó thường nằm ở:

        C: on /mnt/c type drvfs (rw,noatime)

+ Lệnh

        xdg-open /home/<username>/blender_docs/build/html/index.html

    không hoạt động. Bạn sẽ phải chỉnh sửa **.bashrc** bằng cách sử dụng trình soạn văn bản ở chế độ dòng lệnh, tên là *nano* hoặc *vi*, chọn cái nào mà cảm thấy mình quen thuộc nhất - *nano* có lẽ là lựa chọn tốt hơn khi bạn không thực sự cần phải học nhiều và danh sách phím tắt ở phía dưới sẽ giúp bạn bắt đầu nhanh hơn - và tạo một biến môi trường ở cuối tập tin, giống như sau:

        export WIN_HOME=/mnt/c/Users/<windows_account_name>

    bản **.bashrc** trong Linux, Unix, macOS cũng tương tự như chức năng của bản *autoexec.bat* trong các phiên bản **Windows** cũ, nó khởi động khi mình bật cửa sổ dòng lệnh lên, nên tất cả các biến môi trường và dòng lệnh trong đó sẽ được thi hành trước, trước khi chúng ta sử dụng dòng lệnh.

    Địa điểm này giống hệt %userprofile%. Nạp lại **.bashrc** tại dấu nhắc lệnh:

        . ./.bashrc

    sau đó thay đổi thư mục làm việc hiện tại sang **$WIN_HOME** :

        cd "$WIN_HOME"

    trước khi bắt đầu phần tiếp theo để xuất kho mã nguồn viết tài liệu.

    Một khi `make html` đã được thực hiện, bạn có thể sử dụng trình duyệt mạng của bạn để tiếp cận thư mục blender_docs tại **\%userprofile\%**  của bạn và xem tập tin `index.html` tại thư mục **blender_docs**. Sau khi xem, bạn có thể đánh dấu địa chỉ trang trên *Dấu trang ưa thích* (Favorite Bookmarks) của trình duyệt mạng, cho phép bạn truy cập trang này nhanh hơn ở những lần sau.

------------------

## Đăng ký tài khoản và tham gia làm một người đóng góp vào đề án (Registering an user account and join to become a Project's collaborator)

- Vào trang [này](https://github.com/):

- Bấm nút **Sign up**

- Điền tên người dùng vào ô **Username**. Nên dùng kiểu sau: hoangduytran1960 (không có dấu và không có khoảng trống cách chữ, cộng với năm sinh hoặc một số nào đấy)

- Điền thư điện tử vào ô **Email address**

- Điền mật mã vào ô 'Password' (nhớ ghi lại vào đâu đó để về sau có quên thì lấy lại được) (Yêu cầu: 8 ký tự trở lên, gồm A-Z, 0-9, và có chữ Hoa, chữ Thường)

- Bấm **Verify** và xem xem nó bảo làm gì để nó biết là mình không phải là thông tin từ máy mà là người thật.

- Sau khi làm xong thì báo cho tôi biết tên người dùng vào e-mail của tôi [hoangduytran1960@gmail.com](mailto:hoangduytran1960@gmail.com) để tôi thêm vào làm người hợp tác  (collaborator) và đặt quyền cho bạn được gửi các thay đổi lên đề án này.

## Cài đặt các phần mềm cần thiết (Install required softwares)

Làm theo hướng dẫn ở trang [Cài Đặt -- Install](https://docs.blender.org/manual/vi/dev/about/contribute/install/index.html) chọn hệ điều hành tương thích với cái mình đang sử dụng). Ví dụ lấy các phần mềm cần có xuống máy dưới đây là trong hệ điều hành Linux Ubuntu/Mint:

        sudo apt-get install python python-pip git subversion


## Lấy bản nguồn này xuống máy (Downloading the project's source code and documents)

+ Bằng dòng lệnh:

        cd $HOME
        git clone https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git

+ Nếu cài Hệ Thống Phụ Linux (**WSL**) thì dùng:

        cd $WIN_HOME
        git clone https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git

+ Các thư mục sẽ tạo trong ổ cứng là

        blender_manual/
        ├── blender_docs

+ Trong thư mục `blender_manual` mình sẽ tìm thấy thư mục `.git`. Thư mục này là thư mục `git` sử dụng để lưu các thay đổi của mình, cùng có các thư mục khác như `info/exlude` mà mình sẽ nói đến sau này.

+ Tất cả các bài có nội dung tiếng Việt cần sửa, dịch nằm ở trong thư mục:

        $HOME/blender_manual/blender_docs/locale/vi/LC_MESSAGES

+ Thư mục `blender_manual/blender_docs` là thư mục gốc. Nhớ thay thế `\$HOME` sang `\$WIN_HOME` nếu dùng **WSL**.


## Cài đặt các phần mềm cần thiết cho việc biên tập (Install softwares necessary for compilation)

+ Lấy các phần mềm cần có để biên dịch xuống máy:

        sudo install build-essential git subversion
        cd $HOME/blender_manual/blender_docs
        sudo pip install -r requirements.txt

+ Nếu các bạn gặp khó khăn trong vấn đề về UTF-8 (tiếng Việt) trong khi biên soạn thì đổi sang sử dụng Python3, dùng lệnh:

        which python

    và lệnh:

        which python3

    để tìm xem địa chỉ của 'python' nằm ở đâu. Thường là ở '/usr/bin/'.

+ Lần vào đó và liệt kê để xem tên cụ thể:

        cd /usr/bin
        ls -alF python

    Thường thì mình sẽ thấy là 'python' là kết nối mềm (softlink) của 'python2.7', và 'python3' là kết nối mềm của 'python3.6'

+ Đổi lệnh từ 'python' sang dùng 'python3', để khi đánh 'python' thì hệ điều hành tự động sử dụng 'python3':

        sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
        sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

    Nếu đánh dòng lệnh:

        sudo update-alternatives --config python

    thì mình sẽ thấy bảng liệt kê của các lệnh trong bảng 'alternatives' (những phương án thay thế có thể sử dụng), ví dụ:

        There are 2 choices for the alternative python (providing /usr/bin/python).
        (Có 2 lựa chọn về phương án thay thế Python (chu cấp cho /usr/bin/python).)

| Selection (Lựa Chọn) | Path (Đường Dẫn) | Priority (Ưu Tiên) | Status (Trạng Thái) | Comment (Ghi Chú) |
| --- | --- | :---: | --- | --- |
| *0 | /usr/bin/python3.6 | 2 | auto mode | (chế độ tự động) |
| 1 | /usr/bin/python2.7 | 1 | manual mode | (chế độ thủ công) |
| 2 | /usr/bin/python3.6 | 2 | manual mode | (chế độ thủ công) |

        Press <enter> to keep the current choice[*], or type selection number:
        (Bấm phím <enter> để duy trì lựa chọn hiện tại [*], hoặc điền số mình lựa chọn:)

+ Để đổi lại sử dụng python2.7 thì điền 1, rồi bấm phím Enter, để khi đánh 'python' thì nó sử dụng bản '2.7'. Để đổi lại sử dụng python3.6 thì điền 2, để khi đánh 'python' thì nó sử dụng bản '3.6'. Đánh lệnh:

        man update-alternatives

    để xem bảng hướng dẫn sử dụng.

+ Cài đặt như hướng dẫn nhưng dùng 'pip3':

        sudo apt-get -y install python3-pip
        cd $HOME/blender_manual/blender_docs
        sudo pip3 install -r requirements.txt

+ Biên tập bản tiếng Việt dùng lệnh:

        make -d --trace -w -B -e SPHINXOPTS="-D language='vi'" 2>&1

+ Cài đặt git:

        cd $HOME/blender_manual/blender_docs


+ Đặt tên người dùng:

        git config --global user.name "Tên đầy đủ"

+ Đăt địa chỉ e-mail:

        git config --global user.email "địa-chỉ@máy-chủ.com"

+ Những thông tin này thường được ghi ở tập tin `.gitconfig` ở thư mục **\$HOME**

        [user]
            name = Hoang Duy Tran
            email = hoangduytran1960@googlemail.com
            signingkey = ?????????
        [core]
            editor = gedit -s
        [commit]
            gpgsign = false
        [gpg]
            program = gpg2
        [gui]
            recentrepo = <đường dẫn đến thư mục git>

    Xem ví dụ ở đây [brettz9/.gitconfig](https://gist.github.com/brettz9/8d8b6315f7d8f90edec0)

------------------

## Biến môi trường cần thiết (Important environment variables)

Bạn nên tạo 2 biến môi trường sau và ghi vào trong tập lệnh **.bashrc** để đơn giản hóa việc sử dụng dòng lệnh, tránh việc nhắc đi, nhắc lại. Tập lệnh này nằm ở địa chỉ **\$HOME** của mình:

        export BLENDER_MAN_EN=$HOME/blender_manual/blender_docs
        export BLENDER_MAN_VI=$BLENDER_MAN_EN/locale/vi


<!--  -->
## Cài đặt bản *exclude* để bỏ qua những văn bản không cần thiết (Configuring the *exclude* file to ignore objects)

Để tạo bản html ở máy PC địa phương của mình, lệnh **make** sẽ kiến tạo một số các thư mục, văn bản dành riêng cho mình, song những văn bản, thư mục này không cần thiết phải lưu lại và chúng sẽ thay đổi thường xuyên nữa. Để báo cho **git** bỏ qua chúng thì chúng ta phải biên soạn bản:

        .git/info/exclude

dùng hoặc là **kate**, hoặc là **vi**, hoặc **nano**, và điền nội dung sau ở dưới cùng, sau các dòng khởi đầu bằng *#*:

        blender_docs/build
        *.mo
        *.pyc

lưu các thay đổi, trước khi quay trở lại thư mục **blender_docs** và chạy lệnh:

        git status

để xem danh sách các thay đổi.


------------------

## Quy trình làm việc đề cử, tuy không bắt buộc (Proposed operating procedure)

+ Học thêm về cách sử dụng **git**. Tìm trên mạng dùng từ *hướng dẫn sử dụng git*.
+ Tạo một chi nhánh cho mình để thử nghiệm và nếu cần thì có thể xóa chi nhánh đó đi.

        cd $BLENDER_MAN_EN
        git checkout -b <tên chi nhánh>

+ Sau các sửa đổi thì dùng lệnh sau để chuyển vào kho địa phương của mình:

        git commit -am "Lời miêu tả những thay đổi"

+ Muốn bỏ các thay đổi ở `git_dia_phuong` thì có thể dùng:

        git status

+ Để xem các thay đổi và đường dẫn của các tập tin đã thay đổi.

        git stash

+ Để cất giấu các thay đổi để sau này mình có thể lấy lại nếu muốn.

        git checkout -- <filename>

+ Để bỏ các thay đổi trong tập tin <filename> hoàn toàn, lấy lại nội dung cũ.

        git reset --hard

+ Để bỏ tất cả các thay đổi, không bao giờ lấy lại được nữa. Cẩn thận với lệnh này.

+ Quay trở lại một phiên bản nào đó:

        git log --all --decorate --oneline --graph

    cho mình xem danh sách các thay đổi và thấy số mã của các lần commit, đồng thời cho thấy mũi tên hiện nay đang chỉ vào chi nhánh nào, vào `master` hay một chi nhánh nào đó. Ghi nhớ hoặc dùng chuột quét và chọn số mã đó. Mìn còn có thể bấm chuột phải và chọn 'Copy' để đưa vào bộ nhớ. (Xem cách tạo lệnh viết tắt ở cuối bài để khỏi phải đánh lại các lệnh dài, hay sử dụng, nhiều lần)

        git checkout <số mã phiên bản commit>

    bấm bánh xe chuột xuống để lấy con số mà mình đã chọn ở trên. Nếu đã chọn và 'Copy' vào bộ nhớ dùng bấm chuột phải thì có thể sử dụng bấm chuột phải và chọn 'Paste' để dán số mã từ bộ nhớ ra.

+ Sau nhiều thay đổi thì chuyển vào kho bằng lệnh:

        git commit -am "miêu tả thay đổi"

    hoặc

        git add *
        git commit -m "miêu tả thay đổi"

    hoặc

        git add <tên tập tin>
        git commit -m "miêu tả thay đổi"

    rồi dùng:

        git push --set-upstream origin <tên chi nhánh>

+ Để đưa chi nhánh mới vào kho trên mạng. Nếu đã có rồi thì chỉ cần:

        git push

+ Đưa các thay đổi ở chi nhánh vào `master` (Có thể ghi các lệnh vào một tập lệnh ở thư mục `$HOME/bin` và đánh dấu nó là khả thi hành `chmod u+x <tên tập tin>`):

        cd $BLENDER_MAN_EN
        git checkout master
        git pull https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git <tên chi nhánh>
        git add *
        git commit -m "Cập nhật thay đổi từ chi nhánh sang master."
        git push
        git checkout <tên chi nhánh>

+ Lấy nội dung của một chi nhánh đã tồn tại trên mạng:

        git clone -b <tên chi nhánh> https://<tên người dùng>@github.com/hoangduytranuk/blender_manual.git

+ Xóa chi nhánh:

        git branch -d <tên chi nhánh>

    nếu chi nhánh đã hoàn toàn hội nhập với chi nhánh ở kho trên mạng.

        git branch -D <tên chi nhánh>

    không cần biết là chi nhánh đã hội nhập với kho trên mạng hay không, ép buộc xóa.


------------------

## Dịch các bản PO (Translating PO files)

- Dùng một trình biên soạn văn bản có hỗ trợ định dạng phiên dịch **.po**, như bản **Kate** hoặc **Kwrite**. Trên Windows thì bạn còn có thể tự tạo cho mình một bản định nghĩa định dạng PO nữa, nếu sử dụng [NotePad++](https://notepad-plus-plus.org/). Có mấy từ chìa khóa (keywords):

    + **fuzzy**
    + **msgctxt**
    + **msgid**
    + **msgstr**

- Tìm hiểu thêm về [Định dạng của tập tin PO -- The Format of PO Files](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html).
Trong đó:

    + `#, fuzzy` (**mập mờ**): Nếu dòng có dấu này thì máy phiên dịch sẽ không sử dụng nội dung ở dòng **msgstr** và coi nó như là *không có phiên dịch* hoặc *phiên dịch bị lỗi thời*, *phiên dịch có khả nghi về tính chính xác*. Chỉ xóa dòng này đi khi nào bản dịch là hoàn toàn đúng với bản tiếng Anh. Thêm dòng này vào phía trên dòng cho `msgid` nếu thấy phần phiên dịch là **mập mờ**, đáng khả nghi. Thông thường thì các dòng bắt đầu với ký tự **#** sẽ được coi là dòng *comment* và sẽ bị trình biên dịch bỏ qua.

    + `msgctxt` : Dòng đề **ngữ cảnh** sử dụng. Nếu sử dụng mã Python để thanh lọc **Message.id** (ví dụ, sử dụng **sphynx_int** để đọc nội dung của các bản **.po**, như ví dụ dưới đây), và sau đó, chuyển các **Message** sang dạng **list** và dùng thao tác **sorted** để sắp xếp theo trật tự alphabet, hòng lùng tìm các **id** của các **Message** theo phương pháp **Binary Search** thì **ngữ cảnh** `msgctxt` phải là một phần của khóa lọc và khóa lùng tìm.

            from sphinx_intl import catalog as c
            ..
            po_messages = c.load_po(po_file)

    + `msgid`: Dòng nội dung tiếng Anh. Khi lùng tìm thì phải sử dụng cái này làm khóa chính. Nhớ là khóa này có thể lặp lại. Phải kết hợp với **msgctxt** để tạo khóa duy nhất.
    + `msgstr`: Dòng nội dung trong tiếng Việt (dòng để dịch)

- Các dòng **Comment** luôn luôn khởi đầu bằng ký tự **#**. Các dòng này chỉ có tác dụng trong biên soạn để báo cho mình biết dòng chữ trong **msgid** được tìm thấy ở đâu trong mã nguồn, hoặc trong bản **rst**, và ở ngữ cảnh hoặc dòng nào mà thôi, nó sẽ bị bỏ đi trong quá trình biên dịch.

- Khi dịch thì chớ làm gì thay đổi dòng tiếng Anh, dòng `msgid`. Vì dòng chữ này đã được "bẻ gãy" (xuống dòng) với độ dài tối đa (76 ký tự), lúc sao chép nó vào bộ nhớ để dán lên trang [Google Translate](https://translate.google.com/#view=home&op=translate&sl=en&tl=vi) <a id="google-machine-translation"></a> thì các dấu ngoặc kép `"` có thể gây cản trở cho máy dịch và việc xóa chúng đi có thể là quá phiền toái, bạn nên đánh dòng lệnh sau:

        make gettext

    và vào thư mục **build** để thấy thư mục **locale**. Trong thư mục này sẽ có những tập tin với đuôi **.pot**. Các dòng **msgid** trong tập tin này là một dòng liên tục, không bị xuống dòng. Dùng một thực thể của trình biên soạn văn bản và bật xem văn bản **.pot** tương ứng với tập **.po**, sao chép (Ctrl+C) các dòng **msgid** vào bộ nhớ, trước khi dán (Ctrl+V) vào trang của [Google Translate](https://translate.google.com/#view=home&op=translate&sl=en&tl=vi), phần bên trái dành cho tiếng Anh, và lấy phần phiên dịch ở bên phải để đưa vào dòng **msgstr**, rồi sửa lại các từ nó viết sai và cách đặt câu cú, tránh sao cho quá dập khuôn tiếng Anh để người Việt đọc và cảm thấy quen thuộc. Một số nguồn đối chiếu sau mình có thể sử dụng được trong khi tra cứu và làm việc:

    + [Blender 3D: Noob to Pro](https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro)
    + [Blender 2.80 Reference Manual](https://docs.blender.org/manual/en/dev/getting_started/index.html)
    + [Blender Documentation](https://docs.blender.org/api/blender_python_api_master/info_quickstart.html)
    + [Developer Documentation](https://wiki.blender.org/wiki/Main_Page)
    + [Bản Phiên Dịch Giao Diện Người Dùng VI.PO](https://svn.blender.org/svnroot/bf-translations/trunk/po/vi.po)
        - nhớ đổi 'Text Encoding' (Chế độ Giải/Mã Hóa Văn Bản) của trình duyệt mạng sang 'Unicode' hoặc 'UTF-8' để xem được tiếng Việt có dấu. Trong trình duyệt mạng [Firefox](https://ftp.mozilla.org/pub/firefox/releases/) -- vào thư mục của bản có số phiên bản cao mà lấy cho mình một bản -- cho phép mình đổi chế độ giải mã (Bấm chuột phải ở thanh tiêu đề và chọn bật `Menu` lên, rồi vào `View ‣ Text Encoding ‣ Unicode`)
    + [Bảng Chú Giải Thuật Ngữ -- Glossary](https://docs.blender.org/manual/vi/dev/glossary/index.html)
    + [Youtube - Blender](https://www.youtube.com/user/BlenderFoundation)
    + [Từ Điển: Wiktionary tiếng Việt](https://vi.wiktionary.org/wiki/Trang_Ch%C3%ADnh)
    + [Từ Điển: Soha Tra Từ](http://tratu.soha.vn/)

------------------

## Biên tập và xử lý hậu kỳ các thay đổi (Compiling and post processing changes)

+ Các tập tin mới được tạo sẽ chứa một số từ cần điền cho tác giả và ngày sửa đổi v.v. Nếu bạn cảm thấy công việc thay thế chúng lặp đi lặp lại, tẻ nhạt, thì hãy sử dụng tập lệnh

        change_placeholders.sh

    trong thư mục nhánh

        blender_docs/toos_maintenance

+ Sao lấy một bản vào thư mục **bin** địa phương của bạn và thay tất cả các giá trị đề cập trong tập tin với các chi tiết cụ thể của mình, rồi sau mỗi lần thay đổi một tập tin phiên dịch, bạn nên thực hiện các lệnh sau:

        $HOME/bin/change_placeholders.sh $BLENDER_MAN_VI
        make -d --trace -w -B -e SPHINXOPTS="-D language='vi'" 2>&1

+ Xem các thay đổi ở địa phương bằng cách dùng trình duyệt mạng, vào thư mục

        $BLENDER_MAN_EN/build/html/index.html

+ Nên lưu địa chỉ này vào mục ưa thích (Favorites) (Ctrl+D) của trình duyệt mạng để lần sau cứ vào đấy bấm vào để xem trang đầu, F5 (làm tươi lại - refresh) để lấy các thay đổi gần đây nhất mà không phải mở lại


### Nhập kho các thay đổi (Committing changes to repository)

+ Khi thay đổi xong và muốn nhập kho thì làm như sau:

    1. Xem các thay đổi:

            git status

    2. Nhập kho vào ổ địa phương:

        + Báo cho git biết là không ký lần nhập kho bằng mật mã riêng của cá nhân. Chỉ làm một lần.

                git config commit.gpgsign false

        + Báo cho git là lưu trữ tên người dùng và mật mã, dùng cho những lần sau. Chỉ làm một lần.

                git config credential.helper store

+ Đưa vào kho địa phương ở máy

        git commit -am "<ghi chú về những gì đã làm trong thay đổi vừa rồi>"

+ Chuyển giao các thay đổi vào kho trên mạng

        git push

### Cập nhật các thay đổi ở chi nhánh chính **master**

+ Lấy các thay đổi ở tất cả các chi nhánh trên mạng về máy mình, sử dụng:

        git pull --all

+ Sau mỗi lần `git commit` thì thi hành `git pull` để hội nhập các thay đổi ở máy chủ trên mạng với máy mình.

------------------

## Các tập lệnh có thể cần sử dụng (Favourable scripts)

Trong khi làm việc, việc tái thi hành lệnh đã làm trước đây sẽ là một việc không tránh khỏi, chẳng hạn như lệnh tạo *html*. Tốt nhất là kèm chúng vào một tập lệnh ở thư mục **bin** địa phương và đặt nó là có quyền thi hành:

1. Tập lệnh *Python* - **makevidoc.py**:

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



    + Lưu tập lệnh `makevidoc.py` này vào thư mục **\$HOME/bin** của máy. Nếu thư mục này chưa có thì làm theo các lệnh sau: (Có thể thay **\$HOME** sang **\$WIN_HOME** để có thể biên soạn các tập lệnh bằng các trình biên soạn văn bản của riêng mình một cách dễ dàng.)

            cd $HOME
            mkdir bin

    + Nhớ biên soạn bản `·bashrc` và đặt dòng sau để thư mục **\$HOME/bin** nằm trong danh sách các đường dẫn mà hệ điều hành sẽ lùng tìm các bản tập lệnh khi chạy dòng lệnh:

            export MYBIN=$HOME/bin
            export PATH=$MYBIN:$PATH


    + Đặt tập lệnh này là **Khả Thi Hành** (executable) bằng lệnh:

            chmod u+x $HOME/bin/makevidoc.py

    + Sau đó, chúng ta có thể chạy nó như các ví dụ sau:


        - Xem hướng dẫn sử dụng

                makevidoc.py --help

        - Thi hành *make* nhưng không xóa bản cũ đi, viết đè lên. Phương pháp này sẽ nhanh hơn, song nhiều khi sẽ không cho kết quả chính xác:

                makevidoc.py

        - Thi hành *make* và xóa bản cũ đi:

                makevidoc.py -c

        - Thi hành **make** và xóa bản cũ đi, định thư mục nơi nó cần làm việc là thư mục hiện tại ($PWD = Print Working Directory: In ra thư mục làm việc):

                makevidoc.py -c $PWD

2. Tập lệnh **change_placeholders.sh**

    + Tập lệnh này nằm trong thư mục:

            blender_docs/toos_maintenance


        + Sao lấy một bản vào thư mục **\$HOME/bin** của mình và đặt tập lệnh thành **Khả Thi Hành** (executable) như nói ở trên.

        + Tập lệnh này cho phép mình điền tên và e-mail của mình vào phần *COMMENT* của các văn bản mà mình sửa, đồng thời điền ngày giờ mình đã làm nữa. Nó dùng lệnh `svn` và `git` để tìm các văn bản có đuôi là `.po` đã thay đổi. Nếu phải tự lùng tìm ở một thư mục nào đó không phải là thư mục có thư mục `.svn` hoặc `.git` thì nó sẽ tìm các văn bản có đuôi là `.po` mà thôi và cách này là cách làm việc lâu nhất.

        + Các từ mình cần điền chi tiết của cá nhân là:

                YOUR_NAME="Họ tên đầy đủ"
                YOUR_EMAIL="địa-chỉ-email@máy_chủ.com"


        + Tập lệnh này thường được thi hành trong những trường hợp mà các văn bản **.po** bị thay đổi do:
            * Bản thân mình biên soạn nó
            * Sau khi thi hành lệnh

                    make update_po


            để cập nhất các thay đổi từ bản tiếng Anh sang, và quá trình này, ngoài việc cập nhật các thay đổi từ các tập tin nguồn `~/blender_docs/manual/*.rst`, nó còn đánh dấu (không xóa đi) những phần văn bản đã bị xóa đi trong bản nguồn, bằng cách đánh dấu các dòng này với tiền tố **\#~**. Tập lệnh **change_placeholders.sh** cũng phát hiện cái này và xóa các dòng có tiền tố **\#~** ra khỏi văn bản **.po**.


3. Các dòng lệnh mình đã đánh trong cửa sổ dòng lệnh được trình xử lý dòng lệnh ghi lại và trong khi làm việc trong cửa sổ dòng lệnh mình có thể

    + Dùng các phim mũi tên *lên*, *xuống* để gọi lại các dòng lệnh đã đánh theo tuần tự. Mũi tên trái/phải sẽ quay trở lại/tiến về trước các ký tự dòng lệnh, `Home` để về đầu dòng, `End` để về cuối dòng, `Backspace`/`Delete` để xóa về trước hoặc sau. `Insert` để đổi chế độ viết đè lên ký tự cũ, hoặc chèn thêm và vị trí con trỏ. Dùng các phím cơ bản này mình có thể gọi lại các dòng lệnh cũ, biên soạn chúng để thi hành lệnh mới với các tham số khác nhau.

    + Lệnh **history** (Lịch Sử) liệt kê lại các lện đã từng đánh và được ghi lại. Số dòng được định trong tập **.bashrc**

            # for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
            HISTSIZE=1000
            HISTFILESIZE=2000


    + Khi số dòng vượt quá hạn định này thì tất cả những dòng lịch sử trước sẽ bị xóa đi và những dòng mới sẽ được bắt đầu lại từ đầu. Nếu có những dòng lệnh đánh mà mình muốn lưu lại vào một tập tin khác thì mình có thể thi hành các lệnh sau - đặt tên cho tập lệnh là `savehistory.sh`:

            #!/bin/bash
            histfile=$HOME/Documents/my_history.txt
            tempfile=$HOME/tmp.txt
            history >> $histfile
            cat $histfile | sort -nu > $tempfile
            mv $tempfile $histfile


    + Nhớ lệnh **sort** có hai tham số:

            -n : numerical, tức so sánh trong khi sắp xếp dùng giá trị số của dòng, hay lấy thứ tự những con số dẫn đầu, tức số dòng.
            -u : unique, xóa đi những dòng hoàn toàn giống nhau, chỉ giữ lại một dòng.


        xem thêm hướng dẫn về lệnh **sort** dùng:

            man sort


        vì lệnh này sắp xếp cách dòng lệnh theo con số dẫn đầu (số của dòng) (tham số **-n** của lệnh **sort**) và khi HISTSIZE > 1000, nó quay trở lại số 1 thì trật tự sẽ không còn nằm ở dưới, theo tuần tự thời gian mà mình nghĩ là nó sẽ nằm nữa.

    - Khi lệnh **history** (Lịch Sử) liệt kê các dòng lệnh, nó còn liệt kê dòng số ở đầu. Mình có thể gọi lại dòng lệnh bằng cách điền con số dòng với dấu chấm than đứng trước, như sau:

            !<số dòng>
            !123


        và bấm 'Enter'. Lệnh ở dòng số này sẽ được thực hiện (ví dụ thi hành lại lệnh ở dòng số 123)


4. Tập lệnh **.bash_aliases** (Biệt danh)

    - Tập lệnh này sẽ được thi hành bởi tập tin `.bashrc`, nên khi nạp lại tập tin `.bashrc` bằng lệnh `. .~/.bashrc` thì các lệnh biệt danh (viết tắt) cũng sẽ được nạp vào bộ nhớ. Điều tra các lệnh viết tắt bằng cách đánh:

            alias

        và bấm `Enter` để thấy các lệnh được liệt kê.

    - Biên soạn tập tin này để cho các tên viết tắt của các lệnh, chẳng hạn:

            alias graph="git log --all --decorate --oneline --graph"
            alias ll='ls -alF'

        để khi ở dòng lệnh chỉ cần đánh:

            graph
            ll

        thay vì phải đánh toàn bộ.


------------------

## Chuyển thư mục `/home` sang một ổ cứng ngoài

Việc tách riêng hệ điều hành và thư mục $HOME của mình là một thực hành khá tốt, vì khi có vấn đề, hoặc phải cài lại hệ điều hành, thì mình không cần phải lo đến việc cài đặt lại các thông tin ở $HOME của mình. Chỉ việc cài lại hệ điều hành và lắp ổ cứng $HOME vào là có thể làm việc ngay được. Ví dụ sau làm trên hệ điều hành Linux Mint 18.04:

### Cài đặt Linux Mint 18.04:

- Mua lấy một ổ cứng SSD chừng 128GB là thừa đủ. Cũng cần có một ổ cứng ngoài - có thể sử dụng lại ổ cứng cũ nếu không muốn tốn tiền, và sử dụng nó làm ngăn $HOME của riêng mình, cỡ chừng 1TB-4TB.

- Hoặc là dùng một đĩa DVD trắng, hoặc là một thẻ USB, chừng 2GB là đủ

- Vào trang của [Linux Mint](https://linuxmint.com/download.php) và lấy cho mình một bản. Chọn cái xứng hợp với máy của mình. Nếu máy là 64bit thì chọn lấy cái 64bit. Nếu máy vẫn còn là 32bit thì lấy bản dành cho 32bit.

- Tốt nhất là đặt mua đĩa tại [osdisc.com](https://www.osdisc.com/products/linux/linuxmint?affiliate=linuxmint). Giá 1 DVD là $5.95 (Đô-la Mỹ). Tôi chưa đặt qua nên không biết giá cước chuyển về Việt Nam là bao nhiêu. Ở Anh, tôi chỉ mua tạp chí [Linux Magazine](http://www.linux-magazine.com) ở cửa hàng bán báo chí là có cả đĩa kèm theo, song phải nhắm đúng tháng nó in ra đĩa mình mong muốn.

- Nếu định thử phương pháp dùng thẻ USB và máy hiện tại đang sử dụng Windows thì vào [đây](https://sourceforge.net/projects/win32diskimager/files/Archive/Win32DiskImager-1.0.0-binary.zip/download) lấy một bản xuống máy để dùng nó viết tập tin bản Linux Mint mình vừa lấy xuống. Phương pháp an toàn nhất vẫn là sử dụng đĩa DVD mua, tuy chậm hơn.

- Sau khi viết xong thì dùng thẻ USB, hoặc đĩa DVD mà mình đã viết bản Linux Mint lên đó rồi để khởi động máy. Nhớ kiểm tra BIOS của máy để cho phép nó khởi động dùng thẻ USB trước tiên, trước khi chạy ổ cứng.

- Sau khi khởi động, nếu sử dụng ổ đĩa mà mình định sử dụng đã có thông tin ở trong đĩa rồi, thì nên xóa đi bằng cách sau:
    - Bấm tổ hợp phím `Ctrl-Alt F1` để chuyển sang chế độ dòng lệnh.
    - Điền người dùng mặc định là `mint`.
    - Bấm Enter ở dòng hỏi `password:`, không có mật mã.
    - Điền `sudo -s` và bấm `Enter` để vào chế độ người quản lý hệ thống (Administrator, Linux gọi là `root`).
    - Thi hành các dòng lệnh sau:

    1. Liệt kê các ổ cứng, xem cái mình sẽ xóa đi và cài hệ điều hành vào là cái nào, bằng lệnh:

            fdisk -l


        Để ý tên thường là `/dev/sda` hoặc `/dev/sdb` v.v. Ghi nhớ cỡ của ổ cứng để phát hiện cho đúng. Ổ cứng thường có cỡ lớn hơn đĩa và thẻ USB rất nhiều. Nhớ đơn vị cỡ TB (Terabyte) = 1024 GB (Gigabyte), GB = 1024 MB (Megabyte), MB = 1024 KB (Kilobyte), KB = 1024 B (Byte). Giả dụ, ổ đĩa của chúng ta được hệ điều hành gán vào `/dev/sdb', thi hành lệnh:

    2. Xóa các rãnh của ổ cứng cũ. Ví dụ này chỉ xóa 1GB đầu tiên:

            dd if=/dev/zero of=/dev/sdb bs=1G count=1

        để viết 1GB dữ liệu trống ra ổ cứng và xóa trắng 1GB mà thôi. Nếu muốn viết trắng toàn bộ ổ cứng thì viết:

            dd if=/dev/zero of=/dev/sdb bs=1G status=progress

        để xóa trắng tất cả, đưa giá trị của các rãnh về giá trị 0 (`/dev/zero`) và phần mềm sẽ thông báo cho mình biết là nó làm việc đến đâu rồi, cùng tốc độ viết (`status=progress`).

    3. Sau khi viết xong, thi hành:

            partprobe /dev/sdb

        để đọc lại cấu hình của ổ mà mình vừa xóa đi, vì cấu hình, sau khi đã xóa đi, không còn giống như cái cũ trước đây nữa.

    4. Bấm tổ hợp phím `Ctrl-Alt F7` để quay trở lại giao diện đồ họa. Bấm nút 'Install Linux Mint' trên mặt bàn làm việc (desktop) để khởi động cài đặt và điền các thông tin những hướng dẫn trên màn hình. Các bạn có thể chọn ngôn ngữ `tiếng Việt` ở vùng liệt kê danh sách ngôn ngữ trong cửa sổ bên trái và bấm nút `tiếp tục` để thi hành. Theo kinh nghiệm cá nhân, các bạn nên cài bằng tiếng Anh, rồi sau này cài thêm `ibus-unikey` và dùng `ibus` để đánh tiếng Việt thì hơn.


### Cài ổ cứng riêng biệt cho phần $HOME

+ Sau khi cài đặt xong khởi động lại, cắm ổ sẽ dùng để làm $HOME vào.
+ Nếu ổ cứng mình là một ổ cũ và sử dụng hệ thống tập tin khác với những cái thuộc Linux, như `ext4`, thì nên sử dụng phần mềm `disks` (Đĩa) để định dạng (format) nó.

+ Khi đã đăng nhập thì bật `Terminal` lên và thi hành các lệnh sau:

        sudo fsdisk -l

    để vào chế độ người quản lý hệ thống và xem các ổ cứng, nhất là ổ dùng để làm $HOME gọi là gì.

+ Nếu ổ cứng chưa được chuẩn bị thì sử dụng công cụ `disks` để định dạng (format) nó. Nên sử dụng hệ thống tập tin `ext4` (mặc định của Linux) thì hơn. Nhớ để ý chỉ danh `/dev/sd?` xem hệ điều hành gán cho nó là ổ gì. Các đơn giản với các ổ USB là bật `disks` lên và rút ổ ra/cắm ổ vào và xem sự thay đổi của danh sách.

    - Ví dụ, liệt kê ổ cứng:

            sudo fdisk -l
            [sudo] password for <username>:

                Disk /dev/sda: 111.8 GiB, 120034123264 bytes, 234441647 sectors
                Units: sectors of 1 * 512 = 512 bytes
                Sector size (logical/physical): 512 bytes / 512 bytes
                I/O size (minimum/optimal): 512 bytes / 512 bytes

    - Biên soạn đĩa bằng lệnh `fsdisk`:

            sudo fdisk /dev/sda

                Welcome to fdisk (util-linux 2.31.1).
                Changes will remain in memory only, until you decide to write them.
                Be careful before using the write command.

                Device does not contain a recognised partition table.
                Created a new DOS disklabel with disk identifier 0xe7e87b15.

    - In thông tin bằng lệnh `p` (Print):

            Command (m for help): p

                Disk /dev/sda: 111.8 GiB, 120034123264 bytes, 234441647 sectors
                Units: sectors of 1 * 512 = 512 bytes
                Sector size (logical/physical): 512 bytes / 512 bytes
                I/O size (minimum/optimal): 512 bytes / 512 bytes
                Disklabel type: dos
                Disk identifier: 0xe7e87b15

    - Kiến tạo phần ổ cứng mới bằng lệnh `n` (New):

            Command (m for help): n
                Partition type
                p   primary (0 primary, 0 extended, 4 free)
                e   extended (container for logical partitions)
                Select (default p): p (Chọn primary)
                Partition number (1-4, default 1):
                First sector (2048-234441646, default 2048):
                Last sector, +sectors or +size{K,M,G,T,P} (2048-234441646, default 234441646):
                Created a new partition 1 of type 'Linux' and of size 111.8 GiB.

    - Viết ra ổ cứng những thay đổi đã làm:

            Command (m for help): w
                The partition table has been altered.
                Calling ioctl() to re-read partition table.
                Synching disks.


    - Định dạng hệ thống tập tin cho phần ổ cứng vừa tạo sử dụng sắp đặt mặc định, để ý UUID (Universally Unique Identifier) mà hệ điều hành gán cho nó:

```bash
            sudo mke2fs -t ext4 /dev/sda1

                mke2fs 1.44.1 (24-Mar-2018)

                Creating filesystem with 29304949 4k blocks and 7331840 inodes
                Filesystem UUID: f98b7efa-08fd-40a2-8f6d-94388c453b0d
                Superblock backups stored on blocks:
                    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
                    4096000, 7962624, 11239424, 20480000, 23887872

                Allocating group tables: done
                Writing inode tables: done
                Creating journal (131072 blocks): done
                Writing superblocks and filesystem accounting information: done
```

+ Để liệt kê các thông tin này dùng lệnh

        sudo blkid /dev/sda1
            /dev/sda1: UUID="f98b7efa-08fd-40a2-8f6d-94388c453b0d"  TYPE="ext4"

+ Đổi nhãn hiệu để dễ nhận biết hơn bằng lệnh:

        sudo e2label /dev/sda1 "MY_HOME"

+ Sao chép dòng thông tin về ổ mà mình sẽ sử dụng, chẳng hạn như `/dev/sdc1` ở trên.

+ Tạm thời vào địa chỉ của ổ cứng, xem điểm `mount` ở đâu. Nếu dùng `disks` thì bấm nút mũi tên đen bên dưới để `mount` nó và xem điểm `mount` là ở đâu. Thường là

+ Biên soạn `/etc/fstab` để đưa thông tin này vào đó, đặt ánh xạ sang ổ `/home` cho nó như sau:

        nano /etc/fstab

    và điền dòng sau vào cuối cùng:

        UUID=d21aebfe-716e-11e2-97f7-001a64633f00   /home   ext4    defaults    0   2

    nhớ xóa các ngoặc kép ở giá trị của `UUID`

------------------

## Một số phương pháp có thể sử dụng để tăng hiệu suất làm việc

### Dùng máy phiên dịch Google

Cái này đã nói đến ở [trên](#google-machine-translation) rồi, vào trang [Google Translate](https://translate.google.com/#view=home&op=translate&sl=en&tl=vi) và thi hành làm như hướng dẫn

### Tăng lượng dòng định nghĩa từ gõ tắt trong bản macro của Unikey

+ Bản ibus-unikey ở kho lấy về có một giới hạn về số từ viết tắt trong bảng macro có thể ghi và nạp vào bộ nhớ là 1024 dòng, mỗi dòng là một định nghĩa. Tôi có viết thư cho anh Lê Quốc Tuấn, chủ nhân của phần mềm này, và làm theo sự hướng dẫn của anh, [vào đây](https://github.com/vn-input/ibus-unikey) lấy bản mã nguồn dùng lệnh:

        sudo apt-get install -y cmake g++ make pkg-config libibus-1.0-dev libgtk-3-dev
        cd $HOME
        mkdir sources/
        cd sources
        git clone https://github.com/vn-input/ibus-unikey.git
        cd ibus-unikey
        kwrite ukengine/keycons.h

+ Đổi dòng:

        #define MAX_MACRO_ITEMS 1024

    thành

        #define MAX_MACRO_ITEMS 1024 * 4

    Tức tăng số dòng macro có thể sử dụng lên thành 4 lần (4096 dòng). Lưu thay đổi và quay trở lại dòng lệnh:

        mkdir build
        cd build
        cmake -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=release -DLIBEXECDIR=/usr /lib/ibus ..
        make
        sudo make install

+ Bấm chuột phải ở biểu tượng Unikey trên thanh tác vụ và chọn 'Restart' để tắt bản cũ đi, lấy bản mới vào bộ nhớ. Hoặc là biên soạn bản 'macro.txt' và cho thêm từ vào đó, rồi 'Import' nó vào hoặc 'import' từ một bản định nghĩa khác đã có vào. Sau khi 'Save' (Lưu) thì có thể vào thư mục '$HOME/.ibus/unikey' và kiểm tra số dòng của bản 'macro' trong đó, bằng

        cat macro | wc -l

    hoặc dùng:

        kwrite macro

    và kiểm tra số dòng mà phần mềm đã ghi. Hơn 1024 là được.

+ Nhớ mỗi lần thay đổi nội dung của 'macro' trong bộ nhớ thì phải dùng phím chuyển ngôn ngữ (giữa tiếng Anh và tiếng Việt) để đổi sang tiếng Anh rồi quay trở lại tiếng Việt, để kích hoạt bản định nghĩa macro mới.

+ Cách biến quá trình nhập các 'macro' mới vào

        .ibus/unikey/macro

    và khởi động lại **ibus-engine-unikey** tự động, sau mỗi lần thay đổi, hoặc điền thêm định nghĩa vào là dùng **kate** hoặc **kwrite** viết một bản mã **bash shell** tương tự như sau đây và đặt tên cho nó là **refresh_unikey.sh** chẳng hạn, ví dụ bản **macro.txt** nằm trong thư mục *~/Documents*:

        #!/bin/bash
        pkill -9 ibus-engine-uni
        cp -a ~/Documents/macro.txt ~/.ibus/unikey/macro
        chmod 664 ~/.ibus/unikey/macro
        /usr/ibus-engine-unikey --ibus &

    nhớ đổi chế độ cho bản **refresh_unikey.sh** sang bao gồm quyền thi hành, bằng dòng lệnh

        chmod u+x refresh_unikey.sh

    Nhớ là sau khi chạy lệnh **refresh_unikey.sh** ở dòng lệnh thì phải bấm `Ctrl+Spacebar` hai lần đề nó chuyển sang tiếng Anh, rồi tiếng Việt. Cách làm này sẽ giảm thiểu việc chúng ta phải vào trình đơn và dùng lệnh **import**.


### Sử dụng microphone và chức năng dịch giọng nói đánh thành chữ của Google

Chức năng này trong bản 'chromium' - bản nguồn mở - lấy ở kho không hoạt động, tuy hình microphone xuất hiện, song khi bấm vào đó thì nó sẽ nói 'no internet connection' và cho dù mình sửa đổi sắp đặt trong mục

    Settings ‣ Advanced ‣ Privacy and security ‣ Content settings ‣ Microphone

và chọn 'Built-in Audio Analogue Stero' đi chăng nữa.

Chúng ta phải cài đặt 'Chrome' bản chính, như hướng dẫn [ở đây](https://www.tecmint.com/install-google-chrome-in-debian-ubuntu-linux-mint/),

1. Cách thứ nhất là:

        cd Downloads
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
        sudo apt-get update
        sudo apt-get install google-chrome-stable

2. Cách thứ hai là:

        cd Downloads
        wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo dpkg -i google-chrome-stable_current_amd64.deb

    + Sau đó vào trình đơn 'Internet' của hệ điều hành và bấm thi hành 'Google Chrome' hoặc khởi động nó từ dòng lệnh:

            google-chrome-stable &

    + Bấm vào nút ba chấm ở bên phải của dòng địa chỉ, sát mép cửa sổ và vào thư mục:

            Settings ‣ Advanced ‣ Privacy and security ‣ Content settings ‣ Microphone

        bật nút 'Block' (Ngăn chặn) để nó chuyển thành 'Ask before accessing (recommended)' (Hỏi trước khi truy cập (đề cử))

    + Nếu máy có nhiều microphone thì có thể bấm vào nút ở đó và chọn cái mình muốn sử dụng.

    + Bật một 'Tab' mới (bấm dấu '+' ở trên cùng, hoặc bấm 'Ctrl+T'), và bấm vào nút hình cái microphone ở bên phải ở dòng đề 'Search Google or type a URL' (Tìm kiếm Google hoặc đánh máy chữ một dòng địa chỉ URL). Hình biểu tượng microphone màu đỏ hiện ra và bên trái dòng chữ chuyển từ 'Speak now..' (Nói đi) sang 'Listening' (đang lắng nghe). Nói một vài chữ tiếng Anh như 'Hello', hoặc 'Thank you', để nó tìm cho mình. Mình sẽ thấy các chữ ấy được sử dụng để tìm các trang và phim ảnh liên quan đến các chữ mình nói.

    + Lần đến trang [Trình biên soạn văn bản của Google trên mạng](https://docs.google.com/document) và bấm vào nút dấu cộng '+' để lấy một bản tài liệu mới. Bấm vào

            File ‣ Language ‣ Tiếng Việt

    + Để nó luôn luôn sử dụng tiếng Việt trong khi phiên dịch. Bấm vào nút 'Tools' (Các Công cụ) ở trình đơn và chọn 'Voice typing' (Đánh máy chữ bằng giọng nói). Hình biểu tượng cái microphone sẽ hiện ra ở bên trái lề. Nếu thấy nút ở trên hình cái microphone vẫn còn đề là 'English' thì bấm vào đó và chọn đổi sang 'Tiếng Việt' để đổi ngôn ngữ nó lắng nghe và phiên dịch. Phần mềm sẽ tự lưu các sắp đặt và nội dung của bản tài liệu mình đang sử dụng, lần sau, khi sử dụng lại thì nó sẽ nhớ là mình sử dụng tiếng Việt. Nhớ lưu lại dòng liên kết (Ctrl+D) và ghi nó vào một thư mục nào đó trong trình đơn Những Ưa Thích (*Favorites*) của mình, để lần sau, mình sử dụng lại thì chỉ cần bấm vào dòng liên kết là đến lại được.

    + Dùng 'Kate' hoặc 'Kwrite' bật một bản dịch mình muốn làm. Xem dòng **msgid** và dịch nhẩm trong đầu, rồi bấm vào nút hình cái microphone (hiện lên màu đỏ) ở trang của [Trình biên soạn văn bản của Google trên mạng](https://docs.google.com/document) và nói dòng đã dịch trong đầu ấy. Nó sẽ đánh ra các chữ mà nó nghĩ là đúng. Sau khi đã nói xong thì bấm vào hình biểu tượng cái microphone và tắt nó đi (màu đen).

    + Nếu cần phải đánh lại một chữ nào thì bấm và chọn chữ ấy (màu xanh dương), rồi nói lại chữ nó đánh sai. Gợi ý, để nó hiểu được những chữ khó, đôi khi phải nói vài từ trong ngữ cảnh đó, chẳng hạn, thay vì chỉ nó 'lý', thì nói 'lý thuyết' hoặc 'lý luận', hoặc để được chữ 'xương', thay vì 'sương' thì nói 'xương lợn', thay vì 'hạt sương'.

    + Dùng chuột quét để chọn và chép (Ctrl+C) nó vào bộ nhớ của máy. Chuyển sang bản mình đang dịch và bấm (Ctrl+V) để dán dòng chữ đã dịch vào. Sửa lại thành kiểu chữ thường hoặc hoa như mình muốn.


### Sử dụng Python để viết lập trình

+ Vì lượng thông tin trong các tài liệu là khá lớn và có thể có nhiều việc nhắc lại, tức là những việc mình có thể tự động hóa bằng lập trình, đồng thời tái sử dụng các chức năng của mã nguồn 'sphynx', mã nguồn được viết trong Python, nữa. Sau khi cài đặt xong thì mã này sẽ nằm trong thư mục:

        /home/htran/.local/bin

    nơi mà các bản thi hành được đặt ở đó, và thư mục:

        /home/htran/.local/lib

    là nơi các bản thư viện nằm.

+ Để khỏi phải lo lắng quá nhiều về mã văn bản UTF-8, mã tiếng Việt sử dụng, thì chúng ta nên chuyển Python sang sử dụng **python3**, như đã nhắc đến [ở đây](#cai-at-cac-phan-mem-can-thiet-cho-viec-bien-tap-install-softwares-necessary-for-compilation).

+ Theo mặc định thì bản **.profile** ở thư mục *$HOME* của mình sẽ có dòng này:

        #set PATH so it includes user's private bin if it exists
        if [ -d "$HOME/.local/bin" ] ; then
            PATH="$HOME/.local/bin:$PATH"
        fi

    và do đó, nếu mình liệt kê biến môi trường **PATH** ra, bằng lệnh:

        echo $PATH

    thì mình sẽ thấy là địa chỉ **$HOME/.local/bin** sẽ được đặt trước tất cả những địa chỉ (thư mục) khác. Điều này có nghĩa là khi trình điều khiển môi trường (ví dụ `/bin/bash`) phiên dịch các dòng mã đánh ở bàn giao tiếp, nó sẽ lùng tìm ở thư mục **$HOME/.local/bin** trước, trước khi đi đến các thư mục khác được nói đến trong biến môi trường **PATH**.

    Nếu không, chúng ta có thể tự mình thêm vào bản **.profile** ở thư mục $HOME của mình, hoặc vào bản **.bashrc** của mình.

+ Kiểm tra xem đường dẫn đến các thư viện của hệ thống Python nằm ở đâu, bằng cách vào cửa sổ dòng lệnh và đánh các lệnh sau:

        python3
        Python 3.6.7 (default, Oct 22 2018, 11:32:17)
        [GCC 8.2.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import sys
        >>> sys.path

    Lệnh này sẽ liệt kê các thư mục mà Python3, khi hoạt động, sẽ lùng tìm các thư viện của nó. Mình có thể điều khiển cái này bằng 2 cách:

    - Điền vào dùng biến môi trường **PYTHONPATH**. Đặt cái này trong bản **.bashrc** của mình bằng dòng:

                export PYTHONPATH=$HOME/.local/lib/python3.6/site-packages:$PYTHONPATH

        xem thêm thông tin về các biến môi trường của Python [ở đây](https://docs.python.org/3/using/cmdline.html?#environment-variables)

    - Điền 2 dòng sau ở đầu bản mã lập trình của mình (*.py), trước khi dùng lệnh **import** hoặc **from <tên> import** :

                import sys
                sys.path.append("/home/<tên tài khoản người dùng>/.local/lib/python3.6/site-packages")

                from sphinx_intl import catalog as c

                ....
                po_doc = c.load_po(po_path)
                ....
                c.dump_po(po_path, po_doc)

        Nên nhớ, lệnh **c.dump_po** trong tập lệnh

                $HOME/.local/lib/python3.6/site-packages/sphinx_intl/catalog.py

        không cho phép mình điều chỉnh cỡ dòng (số lượng ký tự trên một dòng, và nó sử dụng sắp đặt mặc định `width=76`). Để chủ động biến đổi cái này thì mình phải viết lại cụm mã này, ví dụ các dòng sau đây, và đặt `width=0`, để các dòng văn bản trong bản **.po** không xuống dòng nữa:

                def dump_po(self, filename, catalog):
                    dirname = os.path.dirname(filename)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)

                    # Because babel automatically encode strings, file should be open as binary mode.
                    with io.open(filename, 'wb') as f:
                        pofile.write_po(f, catalog, width=0)

    - Trong quá trình **make gettext**, hoặc **make update_po**, các bản viết có đuôi *.rst* trong thư mục `blender_docs/manual` sẽ được biến hóa sang một bước trung gian bằng trình **parser** trong

                .local/lib/python3.6/site-packages/docutils

        cụ thể là bởi hàm

                def publish(self, argv=None, usage=None, description=None,
                settings_spec=None, settings_overrides=None,
                config_section=None, enable_exit_status=False)

        trong bản `core.py` trong thư mục đó. Dòng:

                self.document = self.reader.read(self.source, self.parser, self.settings)

        cung cấp cho chúng ta một bản tài liệu với các mã đánh dấu tương tự như trong ví dụ sau:

                <document source="/home/<tên tài khoản người dùng>/<thư mục đến>/blender_docs/manual/rigging/armatures/posing/bone_constraints/inverse_kinematics/introduction.rst">
                <section ids="introduction" names="introduction">
                <title>
                Introduction
                </title>
                <paragraph>
                IK simplifies the animation process,
                and makes it possible to make more advanced animations with lesser effort.
                </paragraph>
                ...
                </document>

        Bản này đã được 'làm đẹp lại' bằng hàm **prettify** của [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). Mình có thể viết thêm mã vào bản `core.py` để ghi lại mã của các bản **document**, dùng tên văn bản ở dòng:

                <document source="...">

        và sau đó dùng hàm [find_all](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all) để tìm các phần tử của bản tài liệu và phân tách chúng ra, hòng tiếp cận các giá trị. Mã định phần tử sẽ cho phép mình biết được tính chất của chúng trên bản **html** kết xuất.

        Ví dụ, các dòng đầu đề, các dòng mục tiêu đề, tức các dòng được viết đậm, được nhóm trong các mã sau:

        + title
        + field_list
        + term
        + strong
        + rubric
        + bullet_list

        Phân tích các dòng này để lấy lại được các dòng văn bản cũ là một điều không đơn giản. Sử dụng văn bản **.po** và **.rst**, cùng với công nghệ tìm kiếm *mơ hồ* (fuzzy search), chúng ta có thể lấy lại được dòng văn bản gốc, chẳng hạn:

                pip3 install python-Levenshtein

        và sử dụng bằng cách:

                from Levenshtein import distance as DS
                ...
                dist = DS(s1, s2)

        Đọc thêm về Levenshtein [tại đây](https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance)

