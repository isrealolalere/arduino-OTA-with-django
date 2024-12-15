void setup() {
  // put your setup code here, to run once:
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(9, OUTPUT);

  //numbers pin
//  pinMode(6, OUTPUT);     //1
//  pinMode(7, OUTPUT);     //2
//  pinMode(8, OUTPUT);     //3
//  pinMode(9, OUTPUT);     //4
//  pinMode(10, OUTPUT);    //5
//  pinMode(11, OUTPUT);    //6
//  pinMode(12, OUTPUT);    //7


  for(int i=6; i<13; i++){
    pinMode(i, OUTPUT);
  }
  
  // setting 5 as ground pin
  pinMode(5, OUTPUT);

}

void loop() {

  //traffic light

  for(int i=2; i<5; i++){
    digitalWrite(i, HIGH);
    delay(500);
    digitalWrite(i, LOW);
  }
  delay(2000);

  //reverse the light
  for(int i=4; i>1; i--){
    digitalWrite(i, HIGH);
    delay(500);
    digitalWrite(i, LOW);
  }

  
}
