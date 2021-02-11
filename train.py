'''Train script.
'''

from tqdm import tqdm
import torch
from torch.utils.data import DataLoader
from torch.optim import Adam
from torchsummary import summary
from torchvision import transforms

from level_dict import hierarchy
from runtime_args import args
from load_dataset import LoadDataset
from  model import resnet50
from model.hierarchical_loss import HierarchicalLossNetwork
from helper import calculate_accuracy
from plot import plot_loss_acc

device = torch.device("cuda:0" if torch.cuda.is_available() and args.device == 'gpu' else 'cpu')

train_dataset = LoadDataset(image_size=args.image_size, image_depth=args.image_depth, csv_path=args.train_csv,
                            cifar_metafile=args.metafile, transform=transforms.ToTensor())
test_dataset = LoadDataset(image_size=args.image_size, image_depth=args.image_depth, csv_path=args.test_csv,
                            cifar_metafile=args.metafile, transform=transforms.ToTensor())

train_generator = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=args.no_shuffle, num_workers=args.num_workers)
test_generator = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=args.no_shuffle, num_workers=args.num_workers)

model = resnet50.ResNet50()
optimizer = Adam(model.parameters(), lr=args.learning_rate)


model = model.to(device)

HLN = HierarchicalLossNetwork(metafile_path=args.metafile, hierarchical_labels=hierarchy, device=device)


for epoch_idx in range(args.epoch):

    i = 0
    train_epoch_loss = []
    train_epoch_superclass_accuracy = []
    train_epoch_subclass_accuracy = []
    for i, sample in tqdm(enumerate(train_generator)):


        batch_x, batch_y1, batch_y2 = sample['image'].to(device), sample['label_1'].to(device), sample['label_2'].to(device)
        optimizer.zero_grad()

        superclass_pred,subclass_pred = model(batch_x)
        prediction = [superclass_pred,subclass_pred]
        dloss = HLN.calculate_dloss(prediction, [batch_y1, batch_y2])
        lloss = HLN.calculate_lloss(prediction, [batch_y1, batch_y2])

        total_loss = lloss + dloss
        total_loss.backward()
        optimizer.step()
        train_epoch_loss += total_loss.item()
        train_epoch_superclass_accuracy += calculate_accuracy(predictions=prediction[0], labels=batch_y1)
        train_epoch_subclass_accuracy += calculate_accuracy(predictions=prediction[1], labels=batch_y2)



    print(f'Training Loss at {epoch_idx} : {epoch_loss/(i+1)}')
    print(f'Training Superclass accuracy at {epoch_idx} : {sum(train_epoch_superclass_accuracy)/(i+1)}')
    print(f'Training Subclass accuracy at {epoch_idx} : {sum(train_epoch_subclass_accuracy)/(i+1)}')


    j = 0
    test_epoch_loss = []
    test_epoch_superclass_accuracy = []
    test_epoch_subclass_accuracy = []
    for j, sample in tqdm(enumerate(test_generator)):


        batch_x, batch_y1, batch_y2 = sample['image'].to(device), sample['label_1'].to(device), sample['label_2'].to(device)

        superclass_pred,subclass_pred = model(batch_x)
        prediction = [superclass_pred,subclass_pred]
        dloss = HLN.calculate_dloss(prediction, [batch_y1, batch_y2])
        lloss = HLN.calculate_lloss(prediction, [batch_y1, batch_y2])

        total_loss = lloss + dloss

        test_epoch_loss.append(total_loss.item())
        test_epoch_superclass_accuracy.append(calculate_accuracy(predictions=prediction[0], labels=batch_y1))
        test_epoch_subclass_accuracy.append(calculate_accuracy(predictions=prediction[1], labels=batch_y2))


    #plot accuracy and loss graph
    plot_loss_acc(path=args.graphs_folder, num_epoch=epoch_idx, train_accuracies_superclass=train_epoch_superclass_accuracy, train_losses=train_epoch_loss,
                            test_accuracies_superclass=test_epoch_superclass_accuracy, test_accuracies_subclass=test_epoch_subclass_accuracy,
                            test_losses=test_epoch_loss)



    print(f'Testing Loss at {epoch_idx} : {sum(epoch_loss)/(j+1)}')
    print(f'Testing Superclass accuracy at {epoch_idx} : {sum(epoch_superclass_accuracy)/(j+1)}')
    print(f'Testing Subclass accuracy at {epoch_idx} : {sum(epoch_subclass_accuracy)/(j+1)}')



