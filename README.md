# Project: Predictive Modelling for Agriculture

## Objective
- Maximize the yield of different crops depending on the soil characteristics
- Find the feature that predicts the crop the best

## Strategy
- Multi-class classification to group crops given the conditions under which they thrive

## Describing the data

### Descriptive statistics

<div style="display: inline-block; border-top: 3px double; border-bottom: 3px double; padding: 0px;">
    <table style="width:100%; border-collapse: collapse; margin: 0px;">
    <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Nitrogen<br>concentration</th>
      <th>Phosphorous<br>concentration</th>
      <th>Potassium<br>concentration</th>
      <th>PH value</th>
    </tr>
    </thead>
    <tbody>
        <tr>
        <th>mean</th>
        <td>50.6</td>
        <td>53.4</td>
        <td>48.1</td>
        <td>6.5</td>
        </tr>
        <tr>
        <th>std</th>
        <td>36.9</td>
        <td>33.0</td>
        <td>50.6</td>
        <td>0.8</td>
        </tr>
        <tr>
        <th>min</th>
        <td>0.0</td>
        <td>5.0</td>
        <td>5.0</td>
        <td>3.5</td>
        </tr>
        <tr>
        <th>25%</th>
        <td>21.0</td>
        <td>28.0</td>
        <td>20.0</td>
        <td>6.0</td>
        </tr>
        <tr>
        <th>50%</th>
        <td>37.0</td>
        <td>51.0</td>
        <td>32.0</td>
        <td>6.4</td>
        </tr>
        <tr>
        <th>75%</th>
        <td>84.2</td>
        <td>68.0</td>
        <td>49.0</td>
        <td>6.9</td>
        </tr>
        <tr>
        <th>max</th>
        <td>140.0</td>
        <td>145.0</td>
        <td>205.0</td>
        <td>9.9</td>
        </tr>
    </tbody>
    </table>
</div>


### Distribution of concentration values by crop

<div style="display: flex; flex-direction : row;justify-content: space-around; align-items: center; margin-bottom: 10px; gap: 10px;">
    <img src="output/scatters_nitrogen_concentration.png"
        alt="Scatter plot of nitrogen concentration"
        width=400/>
    <img src="output/scatters_phosphorous_concentration.png"
        alt="Scatter plot of phosphorous concentration"
        width=400/>
</div>

<div style="display: flex; flex-direction : row; justify-content: space-around; align-items: center; gap: 10px">
    <img src="output/scatters_potassium_concentration.png"
        alt="Scatter plot of potassium concentration"
        width=400/>
    <img src="output/scatters_ph.png"
        alt="Scatter plot of PH values"
        width=400/>
</div>

### Pairwise-correlations between concentration types

<div style="display: inline-block; border-top: 3px double; border-bottom: 3px double; padding: 0px;">
    <table style="width:100%; border-collapse: collapse; margin: 0px;">
    <thead>
        <tr style="text-align: right;">
        <th></th>
        <th>Nitrogen<br>concentration</th>
        <th>phosphorous<br>concentration</th>
        <th>potassium<br>concentration</th>
        <th>PH value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Nitrogen<br>concentration</th>
            <td>1.00</td>
            <td>-0.23</td>
            <td>-0.14</td>
            <td>0.10</td>
        </tr>
        <tr>
        <th>Phosphorous<br>concentration</th>
        <td>-0.23</td>
        <td>1.00</td>
        <td>0.74</td>
        <td>-0.14</td>
        </tr>
        <tr>
        <th>Potassium<br>concentration</th>
        <td>-0.14</td>
        <td>0.74</td>
        <td>1.00</td>
        <td>-0.17</td>
        </tr>
        <tr>
        <th>PH value</th>
        <td>0.10</td>
        <td>-0.14</td>
        <td>-0.17</td>
        <td>1.00</td>
        </tr>
    </tbody>
    </table>
</div>

## Key findings