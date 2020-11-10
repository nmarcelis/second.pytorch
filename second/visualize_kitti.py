from second.kittiviewer.backend.main import main
from multiprocessing import Process
import second.kittiviewer.frontend
import torch

if __name__ == '__main__':

    print(f"Cuda Available: {torch.cuda.is_available()}")

    main(16666)


    print("Done")
