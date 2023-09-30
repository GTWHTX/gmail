import multiprocessing as mp
import worker
import sup

def main():
    proxy = sup.parse('proxy.txt')
    mail = sup.parse('mail.txt')
    processes = []
    for i in range(1):
        print('Процесс запущен')
        slicer = slice(0+(10*i), 10+(10*i))
        proxy_list = proxy[slicer]
        mail_list = mail[slicer]
        p = mp.Process(target=worker.run, args=(proxy_list, mail_list))
        p.start()
        processes.append(p)
    for p in processes:
        p.join(300)

if __name__ == '__main__':
    main()
    