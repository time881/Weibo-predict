# Weibo-predict
### project of predict Num Weibo Common, repost, and agree</br>
For Weibo predict:</br>
1.I will create the module for each user who's sum of  repost or Common or agree is not 0, this is the first step.</br> 
2.Plan to train each user by their content, date. have a example for repost</br>
  *1) Split the sentence, exclude the usless vocabulary like 'is', 'and', and count vocabulary start with low repost to high respost, 
  and each vocabulary will get most first time respost number as there weight, save as dictionary
  then, have average weight for each sentence by Sum(sentence)/(number of vocabulary) as one condiction*</br>
  *2) Having train with the RandomForestRegressor, 50 times for each and max deep is 4*</br>
3. Predict by Modules. 
