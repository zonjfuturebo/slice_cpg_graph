@main def exec() = {
  loadCpg("cpg.bin")
  val userDefinedMethods = cpg.method
  .nameNot("<global>")
  .nameNot("<operator>.*")
  .nameNot(".*::.*")
  .filter(_.isExternal == false)

for(function <- userDefinedMethods ){
    function.dotPdg.toJsonPretty |> "bad_pdg.json"
}
}
