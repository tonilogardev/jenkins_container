import com.cloudbees.plugins.credentials.SystemCredentialsProvider
import com.cloudbees.plugins.credentials.domains.Domain
import org.jenkinsci.plugins.plaincredentials.StringCredentials
import com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey

def creds = SystemCredentialsProvider.getInstance().getStore().getCredentials(Domain.global())
creds.each { c ->
  if (c instanceof StringCredentials) {
    println "${c.id}: StringCredentials (${c.secret.plainText.length()} chars)"
  } else if (c instanceof BasicSSHUserPrivateKey) {
    println "${c.id}: SSH Key (${c.privateKeySource.getClass().getSimpleName()})"
  } else {
    println "${c.id}: ${c.getClass().getSimpleName()}"
  }
}
