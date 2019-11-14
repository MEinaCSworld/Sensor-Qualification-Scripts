int trigPin = 11;
int echoPin = 12;
float speedofSound = .0343; //cm/us
float t_echo, dist;

void setup() {
  //
  Serial.begin (9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  //
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //Read the signal by counting the pulsewidth
  t_echo = pulseIn(echoPin, HIGH);

  //Speed of sound in Cardiff, CA assumed to be 343 m/s
  //Accounts for distance for trip there and back by dividing by 2
  // Distance = duration/2 X speed of sound ensuring all units match
  // Distance output in meters

  dist = (t_echo/2) * speedofSound;
  //Maximum pulse rate from manufacturer is 25000 us
  if (t_echo < 26000){
    Serial.print(dist,5);
    Serial.print("\n");
  }
  else {
    Serial.print("No Obstacle\n");
  }
  
  delay(60); // 60 ms is quoted minimum measurement cycle time from manufacturer
  
}
