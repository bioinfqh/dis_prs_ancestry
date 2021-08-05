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
  docker: "quay.io/repository/testaccountq/dis_gen_prs_ancestry"
  }
}

workflow make_panel_wdl {
    input {
        String temp = "test"
    }

    call test { input: temp=temp}
}
