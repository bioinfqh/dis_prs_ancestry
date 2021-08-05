version 1.0

task test {
  input {
    String temp
  }

  command {
  }
  output {
  }
  runtime {
  }
}

workflow make_panel_wdl {
    input {
        String temp = "test"
    }

    call make_panel { input: temp=temp}
}
