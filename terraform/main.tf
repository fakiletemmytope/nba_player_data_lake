# create s3 bucket
resource "aws_s3_bucket" "datalake_bucket" {
  bucket = "temmynbaplayerbucket"

  tags = {
    Name = "My bucket"
  }
}


#create aws_glue
resource "aws_glue_catalog_database" "datalake_glue_database" {
  name = "nba_player_database"
}

#create aws_glue_table
resource "aws_glue_catalog_table" "datalake_glue_table" {
  name          = "nba_players"
  database_name = aws_glue_catalog_database.datalake_glue_database.name
  table_type    = "EXTERNAL_TABLE"
  storage_descriptor {
    columns {
      name = "PlayerID"
      type = "int"
    }
    columns {
      name = "FirstName"
      type = "string"
    }
    columns {
      name = "LastName"
      type = "string"
    }
    columns {
      name = "Team"
      type = "string"
    }
    columns {
      name = "Position"
      type = "string"
    }
    columns {
      name = "Points"
      type = "int"
    }
    location      = "s3://${aws_s3_bucket.datalake_bucket.bucket}/raw-data/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
    }
  }

}