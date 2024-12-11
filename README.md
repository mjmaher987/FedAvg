# FedAvg
Reimplement the FedAvg from Scratch



## Introduction
<img src="https://github.com/user-attachments/assets/c3101332-5ae3-427f-b43b-79347a66baa7" alt="image" width="500" />

Federated Learning is a decentralized learning approach that aims to train a global model from clients with local datasets
    
**Global Update:**

w_{t+1} = ∑{k=1}^K (n_k / n) w{t+1}^k

**Local Update (SGD):**

w_{t+1}^k = w_t - η ∇F_k(w)

## Dataset
I've used the CIFAR-10 dataset.

<img src="https://github.com/user-attachments/assets/311c3f50-f0f1-4a4a-a901-10e1f4e18dde" alt='image' width=500/>

## Model Structure
I've used a simple 2-layer CNN.

<img src="https://github.com/user-attachments/assets/b6dbd46f-d553-407b-9003-b992f2144c86" alt="image" width=500/>

## Time Analysis
<img src='https://github.com/user-attachments/assets/61f1effe-22ae-43df-b6b7-cd9c3c01b2f2' alt='image' widt=500/>

## Results
<img src='https://github.com/user-attachments/assets/599123f2-3edf-4ece-8cc9-cdaa6c9e0e91' alt='image' width=500/>

## Discussion and Conclusion
- **Learning Rate**: The learning rate must be carefully tuned as there is an optimal point.  
- **Batch Size**: Larger sizes were faster but less accurate.  
- **Clients**: More clients slowed training and required more rounds and epochs.  
- **Epochs**: Higher epochs improved accuracy but greatly increased time.  
- **Rounds**: Fewer rounds were faster but less accurate.  
- **Optimal**: Moderate settings balanced time and accuracy.  


## References

- **diagrams.net (formerly draw.io)**  
  Available at: [https://www.drawio.com/](https://www.drawio.com/) (Accessed: 2024-12-09)

- Sarkar, S., Agrawal, S., Baker, T., Maddikunta, P. K. R., & Gadekallu, T. R. (2022).  
  *Catalysis of neural activation functions: Adaptive feed-forward training for big data applications*.  
  Applied Intelligence, 52(12), 13364–13383. Springer.

- McMahan, B., Moore, E., Ramage, D., Hampson, S., & y Arcas, B. A. (2017).  
  *Communication-efficient learning of deep networks from decentralized data*.  
  In *Artificial Intelligence and Statistics* (pp. 1273–1282). PMLR.

