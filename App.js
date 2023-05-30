import React, { useState } from 'react';
import { SafeAreaView, TextInput, Text, View, TouchableOpacity } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import styles from './Styles';

export default function App() {
  const [ticker, setTicker] = useState('');
  const [endDate, setEndDate] = useState('');
  const [chartData, setChartData] = useState([]);

  const predictStock = () => {
    const apiUrl = `https://0116-42-106-216-120.ngrok-free.app/predict?ticker=${ticker}&end_date=${endDate}`;
  
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        const predictedValues = data.predictions;
        setChartData(predictedValues);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };
  

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.titleContainer}>
        <Text style={styles.title}>Stock Market Prediction</Text>
      </View>

      <View style={styles.inputsContainer}>
        <TextInput
          placeholder="Ticker"
          value={ticker}
          onChangeText={text => setTicker(text)}
          style={styles.inputTicker}
        />

        <TextInput
          placeholder="End date (yyyy-mm-dd)"
          value={endDate}
          onChangeText={text => setEndDate(text)}
          keyboardType="numeric"
          style={styles.inputDate}
        />

        <TouchableOpacity onPress={predictStock} style={styles.predictButtonContainer}>
          <Text style={styles.buttonText}>Predict</Text>
        </TouchableOpacity>
      </View>

      {chartData.length > 0 && (
        <LineChart
          data={{
            labels: [ticker], // Set the ticker value as the label for x-axis
            datasets: [
              {
                data: chartData,
              },
            ],
          }}
          width={Dimensions.get('window').width - 40} // Adjust the width if needed
          height={200}
          yAxisLabel="$" // Add the desired y-axis label
          chartConfig={{
            backgroundColor: '#0000ff',
            backgroundGradientFrom: '#000000',
            backgroundGradientTo: '#E0FFFF',
            decimalPlaces: 2,
            strokeWidth: 2,
            color: (opacity = 1) => `rgba(255, 127, 80, ${opacity})`,
            style: {
              borderRadius: 5,
              marginTop: 40, // Add margin to move the chart down
            },
            propsForLabels: {
              dx: 0, // Set dx to 0 to center the label horizontally
              dy: 0, // Adjust the dy value to center the label vertically
              fontWeight: 'bold',
            },
            propsForVerticalLabels: {
              dx: 150, // Adjust the dx value to position the label closer or farther from the y-axis line
              dy: 0, // Set dy to 0 to center the label vertically
              fontWeight: 'bold',
            },
          }}
        /> 
      )}
    </SafeAreaView>
  );
}
