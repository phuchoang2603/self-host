# Configure the 'file' storage backend
storage "file" {
  path = "/vault/file"
}

# Configure the listener
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

api_addr = "http://0.0.0.0:8200"

# Other settings
ui                = true
disable_mlock     = false
