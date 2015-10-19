Multithreading
==============

Basic Concepts
--------------
- Một running program gọi là process, mỗi process sẽ có system state của chúng, bao gồm memory, list of open files...
- Thông thường, một process sẽ thực hiện từng câu lệnh theo một thứ tự xác định của control flow, gọi là main thread of the process.
- Một program có thể tạo 1 process mới sử dụng các lib có sẵn như os hay subprocess (os.fork(), subprocess.Popen()). Tuy nhiên, các process này (gọi là subprocess), hoàn toàn chạy độc lập. Nó sẽ có các private system state và main thread.
- Mặc dù các process là isolate, tuy nhiên chúng có thể liên lạc với nhau qua IPC, một trong những thứ phổ biến nhất là IPC là `message passing`. Nguyên bản ban đầu chỉ có `send()` và `recv()` để gửi và nhận message thông qua I/O channel such as a pipe or network socket.
- Multiple process có thể được sử dụng khi bạn cần thực hiện nhiều task cùng một lúc. Tuy nhiên có 1 phương án khác là sử dụng threads. thread tương tự như process, nó cũng có control flow riêng và execution stack. Tuy nhiên, 1 thread hoạt động trong process tạo ra nó, sharing toàn bộ data và system resource. Threads hữu ích khi muốn thực hiện nhiều task đồng thời, nhưng có nhiều syste state cần share giữa các task.
- Khi multiple process or thread được sử dụng, hệ điều hành sẽ chịu trách nhiệm scheduling their work. Điều này được thực hiện bằng cách chia cho mỗi process or thread một slice time và thực hiện xoay vòng giữa các tasks này. Trên các hệ thống CPU nhiều core, hệ điều hành sẽ schedule process giữa các core của CPU, thực hiện process đông thời.
- Viết một chương trình để tận dụng khả năng thực hiện nhiều task đồng thời là 1 thứ khá phức tạp, sự phức tạp chủ yếu nằm ở việc synchronization và access vào shared data. Việc nhiều task update vào 1 cấu trúc dữ liệu có thể dẫn tới corrupt và inconsistent. Để khắc phục, concurrent program phải xác định đc critical sections trong code và thực hiện protect bằng mutual-exclusion
locks.
- Ví dụ, nhiều threads muốn ghi vào cùng 1 file, bạn phải sử dụng mutual exclusion lock để đồng bộ các hoạt động của chúng sao cho khi 1 thread bắt đầu ghi, các thread khác phải chờ cho nó ghi xong thì mới được phép ghi. Code nhìn sẽ như sau:
```
write_lock = Lock()
...
# Critical section where writing occurs
write_lock.acquire()
f.write("Here's some data.\n")
f.write("Here's more data.\n")
...
write_lock.release()
```

Concurrent programming and Python
---------------------------------
- Python hỗ trợ cả message passing and thread-based concurrent programming
- Python sử dụng internal global interpreter lock (the GIL) chỉ cho phép một Python Thread
thực hiện trong 1 thời điểm. Điều này sẽ giới hạn python program chỉ chạy trên 1 core, bât kể hệ
thống cho bao nhiêu core.
- If an application is mostly I/O bound, it is
generally fine to use threads because extra processors aren’t going to do much to help a
program that spends most of its time waiting for events. For applications that involve
heavy amounts of CPU processing, using threads to subdivide work doesn’t provide any
benefit and will make the program run slower (often
much
slower than you would
guess).

multiprocessing
---------------


Interprocess Communication
--------------------------
- Two primary forms of interprocess communication are supported by the multiprocessing module: pipes and queues. Both methods are implemented using message passing. However, the queue interface is meant to mimic the use of queues
commonly used with thread programs
