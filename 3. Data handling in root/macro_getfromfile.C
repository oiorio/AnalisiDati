void macro_getfromfile(string filename="exercise_Likelihood_1.txt"){
  ifstream f(filename);
  float xs;
  while(!f.eof()){
    f >> xs;
    cout << " xs is "<<xs<<endl;
  };
}
