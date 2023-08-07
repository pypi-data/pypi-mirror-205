terraform {
  backend "gcs" {
    bucket = "{{ state_bucket }}"
    prefix = "{{ tfstate_path }}"
  }
}