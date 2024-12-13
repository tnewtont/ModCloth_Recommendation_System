# ModCloth_Recommendation_System
![alt text](https://platform.vox.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/8177601/Screen_Shot_2017_03_15_at_4.24.53_PM.png?quality=90&strip=all&crop=0,2.844141069397,100,94.311717861206/to/img.png)

## The original dataset, under 'df_modcloth.csv', can be found here: https://github.com/MengtingWan/marketBias/tree/master/data

When online shopping, the products are countless, which can confuse the consumer. Thankfully, recommendation systems can help streamline the consumer's shopping experience. This project aims to build a recommendation system for products sold from ModCloth, a brand that specializes in vintage-inspired women's apparel, particularly with dresses. 

## Results
- A simple metric used to determine how well our k-nearest neighbors model performed was checking how many matches it obtained compared to the actual dataset
- Using 300 singular values on the utility matrix yielded the most matches
  
![alt_text](https://i.gyazo.com/311089b21c447695dc7957518c1c2ac2.png)

- The corresponding root-mean squared error (RMSE) between the original utility matrix and its reduced version is about 0.05572

![alt text](https://i.gyazo.com/a05d24d1060f1803eadc6d57c44e402a.png)

## Data Notes
- Preprocessing and wrangling are done in the 'rsp_data_wrangling.ipynb' notebook
- Utilized four features including:
  - item_id
  - user_id
  - rating
  - category
- Imputed one missing entry in user_id with 'Unknown'
- Data was filtered to include only products that contained 24 or more reviews
  - This was then subsequently stored as its own dataframe 'df_modcloth_filtered.csv'
- A separate dataframe that contains the most popular items through basic aggregation is stored as 'pop_items.csv'

## Model Notes
- The recommendation system is split into two cases:
  - A user's average rating is 4 or above
  - Otherwise, a user's average rating is below 4
- The k-nearest neighbors model used k = 10 and L2-norm
  - Using L1-norm led to significantly less matches
- Since the ratings are rank-based, Spearman's correlation was utilized
- Implemented a stratified 50/50 train-test split on the dataset
- Applied singular value decomposition (SVD) to the utility matrix
  - Tested singular values of 150, 200, 250, 300, 350, 400, 410, and 425
- Model was trained on Google Colab's L4 GPU
## Future Directions
- Apply sentimental analysis to the item descriptions to fully uncover the bias in the data and observe its potential consequences towards the recommendation system
- Increase the threshold for filtering the data by including items that contain 30 or more reviewes
