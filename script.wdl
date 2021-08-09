version 1.0

task test {
  input {
    String temp
  }

  command {
  python3 dis_calc/get_id_from_vcf.py prs_vcf.vcf
  }
  output {
  }
  runtime {
  docker: "https://github.com/bioinfqh/dis_prs_ancestry"
  }
}

workflow make_panel_wdl {
    input {
        String temp = "test"
    }

    call test { input: temp=temp}
}
