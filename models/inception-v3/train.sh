python tank_train.py \
--data_dir=/home/pva1/deeptank/dataset/inc \
--train_dir=/home/pva1/deeptank/models/inception-v3/snapshots \
--max_steps=50000 \
--subset='train' \
--num_gpus=1 \
--fine_tune=True \
--pretrained_model_checkpoint_path=/home/pva1/deeptank/models/inception-v3/model.ckpt-157585 \
--initial_learning_rate=0.0005 \
--num_epochs_per_decay=30.0 \
--learning_rate_decay_factor=0.16 \
--input_queue_memory_factor=8 \
--batch_size=32