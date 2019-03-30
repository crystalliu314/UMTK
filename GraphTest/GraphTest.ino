#define BUTTON 2

int lastButtonState = 0;
float x,y = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(BUTTON, INPUT);
  
  Serial.begin(9600);
  Serial.println("Begin!");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(BUTTON) == HIGH){
    if(lastButtonState == 1){
      lastButtonState = 0;
      Serial.print("END\n");
    }
    else{
      lastButtonState = 1;
      Serial.print("BEGIN\n");
    }
    delay(500);
  }
  
  //Serial.print("Reading: ");
  Serial.print(random(0, 500));
  Serial.print(", ");
  Serial.println(random(0, 5000));
  delay(100);
}
